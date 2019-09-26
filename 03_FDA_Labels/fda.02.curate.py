from pyspark.sql.functions import to_date, year, month, col
from pyspark.sql.types import IntegerType

####
# CONFIGURATION
####
BUCKET_LANDING = "djm-lake-landing"
BUCKET_CURATED = "djm-lake-curated"

# Read the JSON data as a data frame
landed_data = "s3://"+BUCKET_LANDING+"/fda/drug/label/part-*"
dataframe = spark.read.json(landed_data)

# Data transformation - string to datetime
transformed = dataframe.withColumn(
    "effective_date",
    to_date(
        dataframe.effective_time,
        "yyyyMMdd"
    )
).withColumn(
    "year",
    year(
        col(
            "effective_date"
        )
    ).cast(IntegerType())
).withColumn(
    "month",
    month(
        col(
            "effective_date"
        )
    ).cast(IntegerType())
)

# Store refined data as Parquet
transformed.write.partitionBy(
    "year", "month"
).mode(
    "overwrite"
).parquet(
    "s3://"+BUCKET_CURATED+"/fda-product/"
)
