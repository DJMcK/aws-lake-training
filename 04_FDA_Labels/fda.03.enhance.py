from pyspark.sql.functions import to_date

# Data transformation - string to datetime
transformed = dataframe.withColumn(
    "effective_date",
    to_date(
        dataframe.effective_time,
        "yyyyMMdd"
    )
)

# Store refined data as Parquet
transformed.write.mode(
    "overwrite"
).parquet(
    "s3://"+BUCKET_CURATED+"/fda/drug/label/"
)
