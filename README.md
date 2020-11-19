# Spark_practice
 big data practice use spark 1.6.0

部分参考资料：[图灵程序设计丛书].Spark高级数据分析.第2版（主目录下）

## Basic shell command

创建HDFS上的文件目录

`hadoop fs -mkdir linkage`

将本地文件上传至HDFS的目录下

`hadoop fs -put block_*.csv linkage`

在Hadoop集群上部署spark

`spark-shell --master yarn --deploy-mode client`

在本地计算机上启动本地集群

`spark-shell --master local[*]`

等效于：

`spark-shell`

http://DESKTOP-*****:4040

`:help`

`:h?`

`:historay`

## SparkContext

SparkContext 是一个spark自带对象

查看该对象的所有方法：

`sc.[\t]`

([\t])是tab键

### 创建RDD

RDD 以分区（partition）的形式分布在集群中的多个机器上，每个分区代表了数据集的一个子集。分区定义了Spark 中数据的并行单位。Spark 框架并行处理多个分区，一个分区内的数据对象则是顺序处理。创建RDD 最简单的方法是在本地对象集合上调用SparkContext 的parallelize 方法。

`val rdd = sc.parallelize(Array(1, 2, 2, 4), 4)`

第一个参数代表待并行化的对象集合，第二个参数代表分区的个数。

要在分布式文件系统（比如HDFS）上的文件或目录上创建RDD，可以给textFile 方法传入文件或目录的名称：

`val rdd2 = sc.textFile("hdfs:///some/path.txt")`

我们的记录关联数据存储在一个文本文件中，文件中每行代表一个样本。我们用SparkContext 的textFile 方法来得到RDD 形式的数据引用：

#### val、var

只要在Scala 中定义新变量，就必须在变量名称前加上val 或var。名称前带val 的变量是不可变变量。一旦给不可变变量赋完初值，就不能改变它，让它指向另一个值。而以var 开头的变量则可以改变其指向，让它指向同一类型的不同对象。



## 纽约市出租车分析

### 数据描述：

数据来源：

https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

共有四种出租车，这里选取数据为黄色出租车数据，

数据集为**2020年1月到2020年6月**六个csv文件

数据集在`./data`文件夹下

数据集说明在`./data_dic`文件夹下



<img src="README.assets/image-20201119155925103.png" alt="image-20201119155925103" style="zoom:50%;" />

### 地理数据API：Esri Geometry API

我们有出租车乘客上车点和下车点的经纬度 数据，以及表示纽约各个区边界的矢量数据，这些矢量数据用 GeoJSON 格式存储。因我们需要一个可以解析 GeoJSON 数据并能处理其空间关系的工具。具体来说，就是该工 具可以判断某经纬度所代表的点是否在某个区边界所组成的多边形中。

不幸的是，目前没有一个开源的库正好能满足我们的要求。有一个 GeoJSON 的解析工具 可以把 GeoJSON 转换成 Java 对象，但没有相关的地理空间工具能对转换得到的对象进行 空间关系分析。有一个名叫 GeoTools 的项目，但它的组件和依赖关系实在太多，我们不 希望在 Spark shell 中选用有太多复杂依赖的工具。最后有一个 Java 版本的 Esri Geometry API，它的依赖很少而且可以分析空间关系，但它只能解析 GeoJSON 标准的一个子集，因此我们必须对下载的 GeoJSON 数据做一些预处理。

