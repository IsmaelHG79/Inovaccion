package com.axity

import com.axity.utils.constants._
import com.axity.utils.deltas._
import org.apache.log4j.Logger
import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._


object DataFlowIngestionFull {

  def main(args: Array[String]): Unit = {

    val logger = Logger.getLogger(this.getClass())

    // Dirección dodne se encuentra el archivo avro
    val uriAvroDir = args(0)
    val hiveTable = args(1)
    val idTable = args(2)
    val hiveWriteFormat = args(3)
    val colsToHashID = args(4)
    val uriAvroCrifrasControlDirInput = args(5)
    val uriAvroCrifrasControlDirOutput = args(6)
    val full = args(7)
    val partitions = args(8)
    val dirWriteSparkAppId = args(9)
    val writePartitionBy = args(10).toString
    val SID_TID_EID = args(11).toString


    if(uriAvroDir != null && hiveTable != null && idTable!= null && hiveWriteFormat!=null && colsToHashID!=null && uriAvroCrifrasControlDirInput!=null){

      val writePartitionByList = writePartitionBy.toString.split(",").toSeq
      val lstIdArgs = SID_TID_EID.split(",")
      val cols = colsToHashID.split(",")
      val cols_list = cols.toList
      logger.info("Columnas a hashear")
      logger.info(colsToHashID)
      val SID = lstIdArgs(0)
      val TID = lstIdArgs(1)
      val EID = lstIdArgs(2)

      // init spark
      val spark = SparkSession.builder()
        .appName(String.format("INGESTION-%s", hiveTable))
        .config("spark.sql.autoBroadcastJoinThreshold","-1")
        .config("spark.sql.broadcastTimeout","3000")
        .config("spark.sql.join.preferSortMergeJoin", "true")
        .config("spark.sql.codegen.wholeStage","true")
        .config("spark.sql.inMemoryColumnarStorage.compressed","true")
        .config("spark.sql.codegen","true")
        .config("spark.kryoserializer.buffer.mb","128")
        .config("yarn.resourcemanager.am.max-attempts","1")
        .enableHiveSupport()
        .getOrCreate()

      val sc = spark.sparkContext
      val sparkAppId = sc.getConf.getAppId
      writeFileToHDFS(dirWriteSparkAppId,sparkAppId)

      spark.sparkContext.setLogLevel("ERROR")
      spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")
      spark.conf.set("spark.sql.avro.compression.codec", "snappy")
      spark.conf.set("hive.exec.dynamic.partition", "true")
      spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")

      // load avro as DF
      val avroDeltaDF = spark.read.format("avro").load(uriAvroDir).cache()
      //val avroDeltaDF = spark.read.format("avro").load("/data/RCI/prd/inv_tmp/u2000gpon/subrack/data/20200514_10_105_100_2_Subrack_Report_2020-05-14_06-00-08.avro").cache()
      //val cifras = spark.read.format("avro").load("/data/RCI/prd/inv_raw/hive/ctrl/tx_rci_u2000gpon_subrack/20200514_10_105_100_2_Subrack_Report_2020-05-14_06-00-08.avro").cache()
      val cifra_data = avroDeltaDF.select(ctl_file_date,ctl_file_name).groupBy(ctl_file_name).agg(first(ctl_file_name),count("*").alias(total)).select(ctl_file_name,total)
      val countRead = avroDeltaDF.count()

      // get dates from avro df
      val timestampAvro = avroDeltaDF.select(ctl_file_date).take(1).map(_.getLong(0)).toList.head.toString
      val yearAvro = timestampAvro.toString.substring(0,4)
      val monthAvro = timestampAvro.toString.substring(4,6)
      val dayAvro = timestampAvro.toString.substring(6,8)

      val numPartitions: Int = partitions.toInt

      if(full.toString.trim ==full_str){
        logger.info("process")

        val fullDF = avroDeltaDF.withColumn(ctl_ts,lit(getDateTimeStamp())).cache()

        if (writePartitionBy.equals(year_month)){
          val pre_df = fullDF.withColumn(ctl_year,lit(yearAvro.toInt).cast(IntegerType)).withColumn(ctl_month,lit(monthAvro.toInt).cast(IntegerType)).cache()
          addAutditFields(pre_df,SID,TID,EID,cols_list).coalesce(numPartitions).write.format(hiveWriteFormat).mode(SaveMode.Append).partitionBy(writePartitionByList:_*).saveAsTable(hiveTable)
        }
        else if (writePartitionBy.equals(year_month_day)){
          val pre_df = fullDF.withColumn(ctl_year,lit(yearAvro.toInt).cast(IntegerType)).withColumn(ctl_month,lit(monthAvro.toInt).cast(IntegerType)).withColumn(ctl_day,lit(dayAvro.toInt).cast(IntegerType)).cache()
          addAutditFields(pre_df,SID,TID,EID,cols_list).coalesce(numPartitions).write.format(hiveWriteFormat).mode(SaveMode.Append).partitionBy(writePartitionByList:_*).saveAsTable(hiveTable)
        }
        insertAvroCifrasControlFull(spark,uriAvroCrifrasControlDirInput,uriAvroCrifrasControlDirOutput,countRead,countRead,SID,TID,EID,cifra_data)
      }
      else
        logger.error(error_full)

      spark.close()
    }
    else
      logger.error(error_args)
  }

}