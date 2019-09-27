# TODO: Update with your stack name...
STACK_NAME = "djm"

####
# CONFIGURATION
####
BUCKET_LANDING = STACK_NAME + "-landing"
BUCKET_CURATED = STACK_NAME + "-curated"

# Create a copy of the original FDA Product dataset in our lake
source_path = "s3://"+BUCKET_CURATED+"/fda-product"
source_data = spark.read.parquet(source_path).write.mode(
    "overwrite"
).parquet(
    "s3://"+BUCKET_LANDING+"/fda-product/"
)

# Load the duplicated data as our source for what we are about to transform
product_path = "s3://"+BUCKET_LANDING+"/fda-product"
product_data = spark.read.parquet(product_path)

# Load the indications data for extracted terms
indications_path = "s3://"+BUCKET_LANDING+"/fda-product-indications/comprehendoutput/*.json"
indications_data = spark.read.json(indications_path)

# Join the 2 dataframes based on the common key
merged_data = product_data.join(indications_data.select('id', 'extracted_text'), ['id'])

# Store refined data as Parquet
merged_data.write.partitionBy(
    "year", "month"
).mode(
    "overwrite"
).parquet(
    "s3://"+BUCKET_CURATED+"/fda-product/"
)
