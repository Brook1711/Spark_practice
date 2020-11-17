# Spark_practice
 big data practice use spark 1.6.0

# Basic shell command

创建HDFS上的文件目录

`hadoop fs -mkdir linkage`

将本地文件上传至HDFS的目录下

`hadoop fs -put block_*.csv linkage`

在Hadoop集群上部署spark

`spark-shell --master yarn --deploy-mode client`

在本地计算机上启动本地集群

`spark-shell --master local[*]`

等效于

`spark-shell`

http://DESKTOP-*****:4040

# SparkContext

SparkContext 是一个spark自带对象