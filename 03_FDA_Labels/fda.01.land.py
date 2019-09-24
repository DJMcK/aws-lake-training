from zipfile import ZipFile
from io import BytesIO
from pyspark.sql.functions import explode


####
# CONFIGURATION
####
BUCKET_FDA = "download.open.fda.gov"
BUCKET_RAW = "djm-lake-raw"
BUCKET_LANDING = "djm-lake-landing"


# Deflate
# Function to take the raw zip archives provided by the FDA
# and deflate the JSON contents from it.
def deflate(x):
    stream = BytesIO(x[1])
    archive_objects = ZipFile(stream, "r")
    files = [
        i for i in archive_objects.namelist()
    ]
    data = dict(
        zip(
            files,
            [
                archive_objects.open(file).read() for file in files
            ]
        )
    )
    return next(
        iter(
            data.values()
        )
    )


# Load the raw data as binary files
fda_files = sc.binaryFiles(
    "s3://"+BUCKET_FDA+"/2019-08-10/drug/label/*.json.zip"
)

# Deflate the contents
fda_data = fda_files.map(deflate)

# Store the JSON with GZIP compression
fda_data.saveAsTextFile(
    path="s3://"+BUCKET_RAW+"/fda/2019-08-10/drug/label/",
    compressionCodecClass="org.apache.hadoop.io.compress.GzipCodec"
)

# Read the JSON data as a data frame
raw_data = "s3://"+BUCKET_RAW+"/fda/2019-08-10/drug/label/part-*"
dataframe = spark.read.option(
    "multiLine", True
).option(
    "mode", "PERMISSIVE"
).json(raw_data)

# Explode the Results array to get individual rows for each label
results = dataframe.withColumn(
    "results",
    explode("results")
).select("results.*")

# Save new JSON structure with just results
results.write.mode(
    "overwrite"
).format(
    "json"
).option(
    "compression",
    "gzip"
).save(
    "s3://"+BUCKET_LANDING+"/fda/2019-08-10/drug/label/"
)
