package com.axity
import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object DataFlowIngestion {

  private val concat_column = "concat_column"
  private val date = "filedate"
  private val year = "year"
  private val month = "month"
  private val day = "day"
  private val transaction_status = "TRANSACTION_STATUS"
  private val registry_state = "REGISTRY_STATE"

  def main(args: Array[String]): Unit = {

    val uriAvroDir = args(0)
    val hiveTable = args(1)
    val idTable = args(2)
    val hiveWriteFormat = args(3)
    val colsToHashID = args(4)
    val uriAvroCrifrasControlDirInput = args(5)
    val uriAvroCrifrasControlDirOutput = args(6)
    val full = args(7)
    val partitions = args(8)

    if(uriAvroDir != null && hiveTable != null && idTable!= null && hiveWriteFormat!=null && colsToHashID!=null && uriAvroCrifrasControlDirInput!=null){

      // init spark
      val spark = SparkSession.builder()
        .appName("INGESTION")
        .config("spark.sql.autoBroadcastJoinThreshold","50485760")
        .config("spark.sql.join.preferSortMergeJoin", "true")
        .config("spark.sql.codegen.wholeStage","true")
        .config("spark.sql.inMemoryColumnarStorage.compressed","true")
        .config("spark.sql.codegen","true")
        .config("spark.kryoserializer.buffer.mb","128")
        .enableHiveSupport()
        .getOrCreate()


      spark.sparkContext.setLogLevel("ERROR")
      spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")
      spark.conf.set("spark.sql.avro.compression.codec", "snappy")
      spark.conf.set("hive.exec.dynamic.partition", "true")
      spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")

      import spark.implicits._
      import spark.sql

      val avroDeltaDF = spark.read.format("avro").load(uriAvroDir).cache()
      val avroDeltaDFModified = avroDeltaDF.withColumn(year,avroDeltaDF.col(date).substr(1,4).cast(IntegerType)).withColumn(month,avroDeltaDF.col(date).substr(5,2).cast(IntegerType)).withColumn(day,avroDeltaDF.col(date).substr(7,2).cast(IntegerType)).drop("HASH_ID").cache()
      val columnsToConcat = colsToHashID.split(",").toList
      val avroConcatColumnsDF = generateConcatColumns(avroDeltaDFModified,columnsToConcat).persist()
      val avroDeltaWithHashID = generateHashId(avroConcatColumnsDF,idTable).persist()
      val countRead = avroDeltaWithHashID.count()

      // get dates from delta
      val timestampAvro = avroDeltaWithHashID.select(date).take(1).map(_.getLong(0)).toList.head.toLong
      val yearAvro = timestampAvro.toString.substring(0,4).toInt
      val monthAvro = timestampAvro.toString.substring(4,6).toInt
      val dayAvro = timestampAvro.toString.substring(6,8).toInt

      // get hive last partition

      val hiveQuery = s"SELECT * from ${hiveTable}"
      val hiveDF = sql(hiveQuery).toDF.persist()
      val countHiveDF = hiveDF.count()

      val numPartitions: Int = partitions.toInt

      if(countHiveDF == 0 && full.toString.trim !="full"){

        avroDeltaWithHashID.withColumn(transaction_status,lit("insert")).withColumn(registry_state,lit(getDateTime())).coalesce(numPartitions).write.format(hiveWriteFormat).mode(SaveMode.Append).partitionBy(year,month,day).saveAsTable(hiveTable)
        writeAvroCifrasControl(spark,uriAvroCrifrasControlDirInput,uriAvroCrifrasControlDirOutput,countRead,countRead,0,0)
      }
      else  if(full.toString.trim =="full"){

        val fullDF = avroDeltaWithHashID.withColumn(transaction_status,lit("full")).withColumn(registry_state,lit(getDateTime())).persist()
        fullDF.coalesce(numPartitions).write.format(hiveWriteFormat).mode(SaveMode.Append).partitionBy(year,month,day).saveAsTable(hiveTable)
        val fullCount = fullDF.count()
        writeAvroCifrasControl(spark,uriAvroCrifrasControlDirInput,uriAvroCrifrasControlDirOutput,countRead,fullCount,0,0)
      }
      else if( countHiveDF > 0 && full.toString.trim !="full"){

       val unionDFIncremental = handleIncrementalDeltas(spark,avroDeltaWithHashID,hiveDF,idTable,timestampAvro,yearAvro,monthAvro,dayAvro)
        unionDFIncremental._1.withColumn(registry_state,lit(getDateTime())).coalesce(numPartitions).write.format(hiveWriteFormat).mode(SaveMode.Append).partitionBy(year,month,day).saveAsTable(hiveTable)
        writeAvroCifrasControl(spark,uriAvroCrifrasControlDirInput,uriAvroCrifrasControlDirOutput,countRead,unionDFIncremental._2,unionDFIncremental._3,unionDFIncremental._4)
      }

      spark.close()
    }
    else
      println("not enough arguments")
  }

  def writeAvroCifrasControl(spark: SparkSession,uriAvroCifras:String,uriOutput:String,countRead:Long,countInserts:Long,countUpdates:Long,countDelete :Long): Unit ={

    val avroDeltaDF = spark.read.format("avro").load(uriAvroCifras).cache
    val avroCifrasWithInsertsUpdates = avroDeltaDF.withColumn("READ_COUNT",lit(countRead)).withColumn("INSERT_COUNT",lit(countInserts)).withColumn("UPDATE_COUNT",lit(countUpdates)).withColumn("DELETE_COUNT",lit(countDelete)).cache()
    avroCifrasWithInsertsUpdates.write.format("avro").save(uriOutput)
  }

  def evaluateColumns(myCols: Set[String], allCols: Set[String]) = {
    allCols.toList.map(x => x match {
      case x if myCols.contains(x) => col(x)
      case _ => lit("").as(x)
    })
  }

  def getDateTime():String={
    import java.util.Calendar;
    val dT = Calendar.getInstance()
    val getYear = dT.get(Calendar.YEAR)
    val getMonthTemp  = dT.get(Calendar.MONTH).toInt +1.toString
    val getMonth = if (getMonthTemp.length == 1) s"0${getMonthTemp}" else getMonthTemp
    val getDayTemp = dT.get(Calendar.DATE).toString
    val getDay = if (getDayTemp.length == 1) s"0${getDayTemp}" else getDayTemp
    val getHour = dT.get(Calendar.HOUR_OF_DAY)
    val getMinute = dT.get(Calendar.MINUTE)
    val getSecond = dT.get(Calendar.SECOND)
    s"${getYear}:${getMonth}:${getDay}:${getHour}:${getMinute}:${getSecond}"
  }

  //hash_id
  def sha512(str :String): String ={
    import java.security.MessageDigest
    val hashString = MessageDigest.getInstance("SHA-512").digest(str.getBytes("UTF-8")).map("%02x".format(_)).mkString
    hashString
  }

  def generateConcatColumns(df:DataFrame,columnsToGenerateHashID: List[String]): DataFrame ={
    if(columnsToGenerateHashID.nonEmpty){
      val dfColumnsList = df.columns.toList
      val intersectColumns = dfColumnsList.map(x => x.toUpperCase).intersect(columnsToGenerateHashID.map(x => x.toUpperCase)).map(x => x.toUpperCase)
      val colsToConcat = intersectColumns.map( x => col(x)).toSeq
      val dfWithConcatColumns = df.withColumn(concat_column,concat_ws("", colsToConcat :_*))
      dfWithConcatColumns
    }
    else{
      df.withColumn(concat_column,  lit(""))
    }
  }

  def generateHashId(df:DataFrame,colName:String): DataFrame ={
    val strHash=( str:String) => sha512(str)
    val hashUDF = udf(strHash)
    df.withColumn(colName,hashUDF(col(concat_column))).drop(concat_column)
  }

  def handleIncrementalDeltas(sparkSession: SparkSession,avroDeltaWithHashID:DataFrame,hiveDF :DataFrame,idTable :String, timestampAvro:Long, yearAvro:Int,monthAvro:Int,dayAvro:Int): (DataFrame,Long,Long,Long) ={

    val hiveDFTemp = hiveDF.drop(day,month,year,date).withColumn(date,lit(timestampAvro)).withColumn(year,lit(yearAvro)).withColumn(month,lit(monthAvro)).withColumn(day,lit(dayAvro)).cache()

    val avroColumns = avroDeltaWithHashID.columns.map(x => x.toUpperCase).toSet
    val hiveColumns = hiveDFTemp.columns.map(x =>x.toUpperCase).toSet
    val total = avroColumns ++ hiveColumns

    // df s with the same columns and the same order
    val avroDFWithValidateColumns = avroDeltaWithHashID.select(evaluateColumns(avroColumns,total):_*).cache()
    val hiveDFWithValidateColumns = hiveDFTemp.select(evaluateColumns(hiveColumns,total):_*).cache()

    // generate list of columns to concat
    val generalColumns = avroDFWithValidateColumns.columns.intersect(hiveDFWithValidateColumns.columns).map(_.toUpperCase())//.map(x => col(x))
    val listColumnsSkip = List(date,year,month,day,idTable,registry_state,"FILENAME",transaction_status,concat_column).map(x => x.toUpperCase)
    val columnsDiff = generalColumns.diff(listColumnsSkip)

    // genrate df with concat_column to handle updates
    val avroConcatColumnsDFUpdate = generateConcatColumns(avroDFWithValidateColumns,columnsDiff.toList).distinct().cache()
    val hiveConcatColumnsDFUpdate = generateConcatColumns(hiveDFWithValidateColumns,columnsDiff.toList).distinct().cache()

    // updates
    val hiveConcatList = hiveConcatColumnsDFUpdate.select(concat_column).distinct().collect.toList.map(_.getString(0))
    val validateExist =(item:String,items:List[String])=> items.contains(item)
    val updatesDF = hiveConcatColumnsDFUpdate.join(broadcast(avroConcatColumnsDFUpdate),hiveConcatColumnsDFUpdate.col(idTable)=== avroConcatColumnsDFUpdate.col(idTable),"inner").select(avroConcatColumnsDFUpdate.col("*")).filter(x => !validateExist(x.getAs(concat_column).toString,hiveConcatList)).drop(concat_column,transaction_status).withColumn(transaction_status,lit("update")).cache

    // inserts
    val insertsDF = broadcast(avroDFWithValidateColumns).join(hiveDFWithValidateColumns,avroDFWithValidateColumns.col(idTable)=== hiveDFWithValidateColumns.col(idTable),"left").where(hiveDFWithValidateColumns.col(idTable) isNull).select(avroDFWithValidateColumns.col("*")).drop(transaction_status).withColumn(transaction_status,lit("insert")).cache()

    // homologate columns
    val hiveColumnsTemp = hiveDFWithValidateColumns.columns.map(x => col(x))

    // deletes
    val deleteDFTemp = hiveDFWithValidateColumns.join(broadcast(avroDFWithValidateColumns),hiveDFWithValidateColumns.col(idTable)===avroDFWithValidateColumns.col(idTable),"left").where(avroDFWithValidateColumns.col(idTable) isNull).select(hiveDFWithValidateColumns.col("*")).drop(transaction_status).withColumn(transaction_status,lit("delete")).cache
    val deletesDF = deleteDFTemp.select(hiveColumnsTemp:_*).except(hiveDFWithValidateColumns.select(hiveColumnsTemp:_*)).cache()

    // insert & update & delete
    val unionDF = insertsDF.select(hiveColumnsTemp:_*).union(updatesDF.select(hiveColumnsTemp:_*)).union(deletesDF.select(hiveColumnsTemp:_*)).distinct().cache()

    val insertsCount = insertsDF.count()
    val updatesCount = updatesDF.count()
    val deletesCount = deletesDF.count()
    println("insertsCount ---------------------------------------------------------------------"+insertsCount)
    println("updatesCount ---------------------------------------------------------------------"+updatesCount)
    println("deletesCount ---------------------------------------------------------------------"+deletesCount)
    (unionDF,insertsCount,updatesCount,deletesCount)
  }

}