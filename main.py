from pyspark.sql import SparkSession

appName = "Python Example - PySpark Read CSV"
master = 'local'

# Create Spark session
spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .getOrCreate()

# Convert list to data frame
df = spark.read.option('header',True) \
                .option('multiLine', True) \
                .csv('taxidata')

df.show()

print(f'Record count is: {df.count()}')