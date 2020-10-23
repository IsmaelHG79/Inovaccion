package com.axity.utils

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions.{broadcast, col, concat_ws, lit, udf}
import org.apache.spark.storage.StorageLevel
import com.axity.utils.constants._
import org.apache.spark.sql.types.LongType
import java.util.UUID

object deltas {

  def evaluateColumns(myCols: Set[String], allCols: Set[String]) = {
    allCols.toList.map(x => x match {
      case x if myCols.contains(x) => col(x)
      case _ => lit("").as(x)
    })
  }


  def getDateTimeStamp():String={
    import java.util.Calendar;
    val dT = Calendar.getInstance()
    val getYear = dT.get(Calendar.YEAR)
    val getMonthTemp  = (dT.get(Calendar.MONTH)+1).toString
    val getMonth = if (getMonthTemp.length == 1) s"0${getMonthTemp}" else getMonthTemp
    val getDayTemp = dT.get(Calendar.DATE).toString
    val getDay = if (getDayTemp.length == 1) s"0${getDayTemp}" else getDayTemp
    val getHourTemp = dT.get(Calendar.HOUR).toString
    val getHour = if (getHourTemp.length == 1) s"0${getHourTemp}" else getHourTemp
    val getMinTemp = dT.get(Calendar.MINUTE).toString
    val getMin = if (getMinTemp.length == 1) s"0${getMinTemp}" else getMinTemp
    val getSecTemp = dT.get(Calendar.SECOND).toString
    val getSec = if (getSecTemp.length == 1) s"0${getSecTemp}" else getSecTemp
    s"${getYear}-${getMonth}-${getDay} ${getHour}:${getMin}:${getSec}"
  }
  
  def getDateTimeStampFixed(date:String):String={
    import java.util.Calendar;
    val dT = Calendar.getInstance()
    val getYear = date.toString.substring(0,4)
    val getMonth = date.toString.substring(4,6)
    val getDay = date.toString.substring(6,8)
    val getHourTemp = dT.get(Calendar.HOUR).toString
    val getHour = if (getHourTemp.length == 1) s"0${getHourTemp}" else getHourTemp
    val getMinTemp = dT.get(Calendar.MINUTE).toString
    val getMin = if (getMinTemp.length == 1) s"0${getMinTemp}" else getMinTemp
    val getSecTemp = dT.get(Calendar.SECOND).toString
    val getSec = if (getSecTemp.length == 1) s"0${getSecTemp}" else getSecTemp
    s"${getYear}-${getMonth}-${getDay} ${getHour}:${getMin}:${getSec}"
  }
  
  def getDate():String={
    import java.text.SimpleDateFormat
    import java.util.{Calendar, Date}

    val dateFmt = "yyyyMMdd"
    val date = new Date
    val sdf = new SimpleDateFormat(dateFmt)
    sdf.format(date)
  }

  //hash_id
  def md5(str :String): String ={
    import java.security.MessageDigest
    val hashString = MessageDigest.getInstance(hash_format).digest(str.getBytes("UTF-8")).map("%02x".format(_)).mkString
    hashString
  }

  def generateConcatColumns(df:DataFrame,columnsToGenerateHashID: List[String]): DataFrame ={
    if(columnsToGenerateHashID.nonEmpty){
      val dfColumnsList = df.columns.toList
      val intersectColumns = dfColumnsList.map(x => x.toLowerCase).intersect(columnsToGenerateHashID.map(x => x.toLowerCase)).map(x => x.toLowerCase)
      val colsToConcat = intersectColumns.map( x => col(x)).toSeq
      val dfWithConcatColumns = df.withColumn(concat_column,concat_ws("", colsToConcat :_*))
      dfWithConcatColumns
    }
    else{
      df.withColumn(concat_column,  lit(""))
    }
  }

  def generateHashId(df:DataFrame,colName:String): DataFrame ={
    val strHash=( str:String) => md5(str)
    val hashUDF = udf(strHash)
    df.withColumn(colName,hashUDF(col(concat_column))).drop(concat_column)
  }

  def addAutditFields(df:DataFrame, SID :String, TID:String,EID:String,columnsToGenerateHashID: List[String]): DataFrame ={

    val strHash=( str:String) => md5(str)
    val hashUDF = udf(strHash)

    val generateUUID=()=> UUID.randomUUID().toString
    val uuidUDF = udf(generateUUID)

    val colsToConcat = columnsToGenerateHashID.map( x => col(x)).toSeq
    //val colsToConcat = List("ACTIVO","ETIQUETA","SERIE","LOCATION","ctl_file_date").map( x => col(x)).toSeq
    df.withColumn(ctl_rid,uuidUDF()).withColumn(ctl_sid,lit(SID)).withColumn(ctl_tid,lit(TID)).withColumn(ctl_eid,lit(EID)).withColumn(concat_column,concat_ws("", colsToConcat :_*)).withColumn(ctl_rfp,hashUDF(col(concat_column))).drop(concat_column)

  }

  def writeFileToHDFS(dir:String,file:String): Unit ={
    try {
      val fs = FileSystem.get(new Configuration())
      if (fs.exists(new Path(dir))) {
        fs.delete(new Path(dir), true)
        val os = fs.create(new Path(dir))
        os.write(file.getBytes)
      }
      else{
        val os = fs.create(new Path(dir))
        os.write(file.getBytes)
      }
    }catch {
      case ex: Exception =>
        println(s"Exception: ${ex}")
    }
  }

  def insertAvroCifrasControlODK(spark: SparkSession,uriAvroCifras:String,tableCifras:String,countRead:Long =0 ,countInserts:Long = 0,SID :String, TID:String,EID:String,filename:String, filedate:String): Unit ={
    import org.apache.spark.sql._
    import org.apache.spark.sql.types._

    val dataCifras = List(
      Row(countRead.toLong, filedate.toLong, filedate.toLong, filename)
    )

    val rdd = spark.sparkContext.parallelize(dataCifras)
    val schema = StructType(
      List(
        StructField("rowprocessed", LongType, true),
        StructField("ctl_file_date", LongType, true),
        StructField("dateload", LongType, true),
        StructField("ctl_file_name", StringType, true)
      )
    )
    val cifrasBase = spark.createDataFrame(rdd,schema)
    val avroCifrasWithInsertsUpdates = cifrasBase.withColumn( read_count,lit(countRead)).withColumn(insert_count ,lit(countInserts)).withColumn(update_count,lit(0)).withColumn(ctl_sid,lit(SID)).withColumn(ctl_tid,lit(TID)).withColumn(ctl_eid,lit(EID)).cache()
    avroCifrasWithInsertsUpdates.write.format("hive").mode(SaveMode.Append).saveAsTable(tableCifras)
  }

  def insertAvroCifrasControl(spark: SparkSession,uriAvroCifras:String,tableCifras:String,countRead:Long =0 ,countInserts:Long = 0,SID :String, TID:String,EID:String): Unit ={
    import org.apache.spark.sql._
    //val prueba = spark.read.format("avro").load("/data/RCI/stg/hive/work/ctl/ctrl_tx_unmsnec_aux/20200225_10_32_218_135_PNMSj_rmon_inventory_010_245_244_083_20200225_tx_unmsnec_aux.avro").cache()
    val avroDeltaDF = spark.read.format("avro").load(uriAvroCifras).cache
    //val avroDeltaDF2 = avroDeltaDF.withColumnRenamed("id_table","ctl_tid")
    val avroDeltaDF2 = avroDeltaDF.drop("id_table")
    val avroCifrasWithInsertsUpdates = avroDeltaDF2.withColumn( read_count,lit(countRead)).withColumn(insert_count ,lit(countInserts)).withColumn(update_count,lit(0)).withColumn(ctl_sid,lit(SID)).withColumn(ctl_tid,lit(TID)).withColumn(ctl_eid,lit(EID)).cache()
    avroCifrasWithInsertsUpdates.write.format("hive").mode(SaveMode.Append).saveAsTable(tableCifras)
  }

  def insertAvroCifrasControlFull(spark: SparkSession,uriAvroCifras:String,tableCifras:String,countRead:Long =0 ,countInserts:Long = 0,SID :String, TID:String,EID:String,cifra_data:DataFrame): Unit ={
    import org.apache.spark.sql._
    import org.apache.spark.sql.types._
    import spark.implicits._
    //val prueba = spark.read.format("avro").load("/data/RCI/stg/hive/work/ctl/ctrl_tx_unmsnec_aux/20200225_10_32_218_135_PNMSj_rmon_inventory_010_245_244_083_20200225_tx_unmsnec_aux.avro").cache()
    val avroDeltaDF = spark.read.format("avro").load(uriAvroCifras).cache
    //val avroDeltaDF2 = avroDeltaDF.withColumnRenamed("id_table","ctl_tid")
    val avroDeltaDF2 = avroDeltaDF.drop("id_table")
    val avroDeltaDF3 = broadcast(avroDeltaDF2.as("cifras")).join(broadcast(cifra_data.as("cifras_data")),$"cifras.ctl_file_name" === $"cifras_data.ctl_file_name","inner").select($"cifras.*",$"cifras_data.total")
    val avroCifrasWithInsertsUpdates = avroDeltaDF3.withColumn( read_count,lit(col("total"))).withColumn(insert_count ,lit(col("total"))).withColumn(update_count,lit(0)).withColumn(ctl_sid,lit(SID)).withColumn(ctl_tid,lit(TID)).withColumn(ctl_eid,lit(EID)).drop(total).cache()
    avroCifrasWithInsertsUpdates.write.format("hive").mode(SaveMode.Append).saveAsTable(tableCifras)
  }

}
