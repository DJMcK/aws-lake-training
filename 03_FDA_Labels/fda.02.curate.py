####
# CONFIGURATION
####
BUCKET_LANDING = "djm2-lake-landing"
BUCKET_CURATED = "djm2-lake-curated"

# Read the JSON data as a data frame
landed_data = "s3://"+BUCKET_LANDING+"/fda/2019-08-10/drug/label/part-*"
dataframe = spark.read.json(landed_data)

# Store refined data as Parquet
dataframe.write.mode("overwrite").parquet("s3://"+BUCKET_CURATED+"/fda/drug/label/")
