from pyspark.sql.types import IntegerType, StructField, StructType, StringType

####
# CONFIGURATION
####
BUCKET_LANDING = "djm2-lake-landing"
BUCKET_CURATED = "djm2-lake-curated"

###
#  Given that the source files (CSV files) does not have a header row
#  then we won't be able to infer the schema / data structure.
#  Instead, we must manually define the structure.
###
schema = StructType(
    [
        StructField("label", IntegerType(), True),
        StructField("title", StringType(), True),
        StructField("abstract", StringType(), True)
    ]
)

###
#  Bring in the train data and convert to Parquet
###
training_data = "s3://"+BUCKET_LANDING+"/dbpedia/train.csv.gz"
training_dataframe = spark.read.csv(training_data, header=False, schema=schema)
training_dataframe.count()
training_dataframe.write.mode("overwrite").parquet("s3://djm2-lake-curated/dbpedia/train/")

###
#  Bring in the test data and convert to Parquet
###
test_data = "s3://"+BUCKET_LANDING+"/dbpedia/test.csv.gz"
test_dataframe = spark.read.csv(test_data, header=False, schema=schema)
test_dataframe.count()
test_dataframe.write.mode("overwrite").parquet("s3://"+BUCKET_CURATED+"/dbpedia/test/")
