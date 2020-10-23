package com.axity
import com.axity.DataFlowIngestion.writeAvroCifrasControl
import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object DataFlowIngestionODK {

  private val concat_column = "concat_column"
  private val filedate = "filedate"
  private val year = "year"
  private val month = "month"
  private val day = "day"
  private val transaction_status = "TRANSACTION_STATUS"
  private val registry_state = "REGISTRY_STATE"

  def main(args: Array[String]): Unit = {

    val uriAvroDir = args(0)							// /user/training/odk/
    val hiveTable = args(1)								//tx_odk
    val idTable = args(2)								//hash_id
    val hiveWriteFormat = args(3)						//hive
    val colsToHashID = args(4)							//Id_form,Clave_form,form_element,Atributo
    val fileDateArg = args(5)			//
    val uriAvroCrifrasControlDirOutput = args(6)		//
    val full = args(7)									//full o nofull
    val partitions = args(8)							//6

    if(uriAvroDir != null && hiveTable != null && idTable!= null && hiveWriteFormat!=null && colsToHashID!=null){

      // init spark
      val spark = SparkSession.builder()
        .appName("INGESTION_ODK")
        .enableHiveSupport()
        .getOrCreate()

      spark.sparkContext.setLogLevel("ERROR")
      spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")
      spark.conf.set("spark.sql.avro.compression.codec", "snappy")
      spark.conf.set("hive.exec.dynamic.partition", "true")
      spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")


      val struct =
        StructType(Array(
          StructField("Id_form", StringType, true) ,
          StructField("Clave_form", StringType, true) ,
          StructField("form_element", StringType, true) ,
          StructField("Atributo", StringType, true),
          StructField("no_informe", StringType, true) ,
          StructField("ma", StringType, true)))

      //Read File
      val fileDF = spark.read.option("header", "false").option("delimiter","|").schema(struct).csv(uriAvroDir).cache()
      val countRowsRead = fileDF.count()

      //Add column "filedate" and "filename"
      val avroDeltaDFModified = fileDF.withColumn(filedate,lit(fileDateArg)).withColumn("filename",lit(uriAvroDir))

      //Concat columns
      val columnsToConcat = colsToHashID.split(",").toList
      val avroConcatColumnsDF = generateConcatColumns(avroDeltaDFModified,columnsToConcat).cache()

      //Generate column "Hash_Id"
      val avroDeltaWithHashID = generateHashId(avroConcatColumnsDF,"HASH_ID").cache()

      //Add columns: sourceid, registry_date, datasetName, timestamp and transaction_status
      val avroDeltaWithCols = avroDeltaWithHashID.withColumn("sourceid",lit("ODK")).withColumn(registry_state,lit(getTimeStamp())).withColumn("datasetName",lit("ODK"))
        .withColumn("timestamp",lit(getFileDate())).withColumn(transaction_status,lit("full")).cache()

      //Add columns partitions: year, month, day
      val yearTemp= fileDateArg.substring(0, 4).toInt
      val monthTemp= fileDateArg.substring(4, 6).toInt
      val dayTemp= fileDateArg.substring(6, 8).toInt
      val avroDeltaWithPartCols = avroDeltaWithCols.withColumn(year,lit(yearTemp)).withColumn(month,lit(monthTemp)).withColumn(day,lit(dayTemp))


      if(full.toString.trim =="full"){

        avroDeltaWithPartCols.coalesce(partitions.toInt).write.format(hiveWriteFormat).mode(SaveMode.Append).partitionBy(year,month,day).saveAsTable(hiveTable)
        writeAvroCifrasControl(spark,uriAvroCrifrasControlDirOutput,countRowsRead,countRowsRead,0,0)

      }
      spark.close()
    }
    else
      println("not enough arguments")
  }

  def getFileDate():String={
    import java.util.Calendar
    val dT = Calendar.getInstance()
    val getYear = dT.get(Calendar.YEAR)
    val getMonthTemp = dT.get(Calendar.MONTH).toInt + 1
    val getMonth = if (getMonthTemp.toString.size == 1 ) s"0${getMonthTemp}" else getMonthTemp
    val getDayTemp = dT.get(Calendar.DATE).toString
    val getDay = if (getDayTemp.toString.size == 1 ) s"0${getDayTemp}" else getDayTemp

    s"${getYear}${getMonth}${getDay}"
  }

  def getTimeStamp():String={
    import java.util.Calendar
    val dT = Calendar.getInstance()
    val getYear = dT.get(Calendar.YEAR)
    val getMonthTemp = dT.get(Calendar.MONTH).toInt + 1
    val getMonth = if (getMonthTemp.toString.size == 1 ) s"0${getMonthTemp}" else getMonthTemp
    val getDayTemp = dT.get(Calendar.DATE).toString
    val getDay = if (getDayTemp.toString.size == 1 ) s"0${getDayTemp}" else getDayTemp
    val getHour = dT.get(Calendar.HOUR_OF_DAY)
    val getMinute = dT.get(Calendar.MINUTE)
    val getSecond = dT.get(Calendar.SECOND)
    s"${getYear}:${getMonth}:${getDay}:${getHour}:${getMinute}:${getSecond}"
  }

  def writeAvroCifrasControl(spark: SparkSession,uriOutput:String,countRead:Long,countInserts:Long,countUpdates:Long,countDelete :Long): Unit ={

    import spark.implicits._
    val avroDeltaDF = Seq((countRead,countInserts,countUpdates,countDelete)).toDF("READ_COUNT","INSERT_COUNT","UPDATE_COUNT","DELETE_COUNT")
    avroDeltaDF.write.format("avro").save(uriOutput)
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

}
