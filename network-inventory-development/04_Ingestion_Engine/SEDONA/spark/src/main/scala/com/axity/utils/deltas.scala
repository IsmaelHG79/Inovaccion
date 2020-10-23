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


  def insertAvroCifrasControl(spark: SparkSession,uriAvroCifras:String,tableCifras:String,countRead:Long =0 ,countInserts:Long = 0,SID :String, TID:String,EID:String): Unit ={
    import org.apache.spark.sql._
    //val prueba = spark.read.format("avro").load("/data/RCI/prd/inv_raw/hive/ctrl/tx_rci_fixed_asset/20200301_ACTIVOS_APERTURADOS_MARZO_2020_V2.avro").cache
    val avroDeltaDF = spark.read.format("avro").load(uriAvroCifras).cache
    //val avroDeltaDF2 = avroDeltaDF.withColumnRenamed("id_table","ctl_tid")
    val avroDeltaDF2 = avroDeltaDF.drop("id_table")
    val avroCifrasWithInsertsUpdates = avroDeltaDF2.withColumn( read_count,lit(countRead)).withColumn(insert_count ,lit(countInserts)).withColumn(ctl_sid,lit(SID)).withColumn(ctl_tid,lit(TID)).withColumn(ctl_eid,lit(EID)).cache()
    avroCifrasWithInsertsUpdates.write.format("hive").mode(SaveMode.Append).saveAsTable(tableCifras)
  }
}
