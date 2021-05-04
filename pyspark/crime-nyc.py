from pyspark.sql import SparkSession
from pyspark.sql import functions as func

spark = SparkSession.builder.appName("SparkSQL").getOrCreate()

crime_table = spark.read.option("header", "true").option("inferSchema", "true").csv("file:///SparkCourse/NYPD_Complaint_Data_Historic.csv")

crime_table.createOrReplaceTempView("crime_table")
result = spark.sql("SELECT LAW_CAT_CD, SUBSTRING(CMPLNT_FR_DT, 7, 10) AS year, SUBSTRING(CMPLNT_FR_DT, 1, 2) AS month, COUNT(*) AS cnt \
    FROM crime_table GROUP BY LAW_CAT_CD, month, year HAVING year IN ('2018', '2019', '2020', '2021') ORDER BY year, month, LAW_CAT_CD")

for element in result.collect():
    print(element)

result.write.format('csv').option('header',True).mode('overwrite').option('sep',',').save('crime_result.csv')

spark.stop()