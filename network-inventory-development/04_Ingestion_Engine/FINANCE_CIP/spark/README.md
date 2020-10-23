### Instructions:


Writing your Spark code, then compile the project with the command:

```mvn clean package```

Inside the ```/target``` folder you will find the result fat jar called ```spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-depencencies.jar```. In order to launch the Spark job use this command in a shell with a configured Spark environment:

    spark-submit --master yarn --deploy-mode client --name "Delta SPARK" --class com.axity.DataFlowIngestion /home/fh967x/SparkData/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar /data/RCI/raw/AF/data/ tx_fixed_asset hash_id hive ACTIVO,ETIQUETA,SERIE



Copiar jar al raw rc de att

```scp spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar  raw_rci@10.150.25.146:/home/raw_rci/SPARK```