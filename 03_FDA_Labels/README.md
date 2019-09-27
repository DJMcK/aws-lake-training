# FDA Drug Labels Data

The FDA provides a wealth of large data sets via the [OpenFDA](https://open.fda.gov/) website and APIs. We will leverage one of these data sets in particular; the [Drug Labels](https://open.fda.gov/apis/drug/label/).

## Raw Data

The FDA provides access to all of the [OpenFDA](https://open.fda.gov/) data via a public S3 bucket. We can pull this data in directly using the following command:

```bash
aws s3 sync s3://download.open.fda.gov/2019-08-10/drug/label s3://$STACK_NAME-raw/fda-source/2019-08-10/drug/label
```
> **Windows:** `aws s3 sync s3://download.open.fda.gov/2019-08-10/drug/label s3://%STACK_NAME%-raw/fda-source/2019-08-10/drug/label`

> **Note:** The above command assumes that you have the `STACK_NAME` variable set in your terminal from our setup steps.

## Land Data

**Objectives for this section:**

1. Take the raw `zip` "parts" as an input
2. `deflate` the files and save as `gzip` compressed `json` files - this puts them in a format we can interact with using Spark
3. Read the compressed `json` files as a [DataFrame](https://spark.apache.org/docs/2.2.0/sql-programming-guide.html#datasets-and-dataframes)
4. Select the property we want to extract from the large object
5. `explode` the list of results creating a new structure where each drug is now a row
6. Land the new optimized data set as `gzip` compressed `json` files

**Steps:**

1. Connect to your EMR Cluster (as described in [04_EMR_Cluster](../02_EMR_Cluster/README.md))
2. Run `pyspark --driver-memory 10G --executor-memory 10G --executor-cores 1`
3. Open [`fda.01.land.py`](./fda.01.land.py) in an editor
4. Update the values for `BUCKET_RAW` and `BUCKET_LANDING` with the appropriate values
5. Copy the code and paste it into the `pyspark` shell

## Curate Data

> **Prerequisite:** The output from the [Land Data](#land-data) should be in your "landing" bucket ready for curation.

1. Connect to your EMR Cluster (as described in [02_EMR_Cluster](../02_EMR_Cluster/README.md))
2. Run `pyspark`
3. Open [`fda.02.curate.py`](./fda.02.curate.py) in an editor
4. Update the values for `BUCKET_LANDING` and `BUCKET_CURATED` with the appropriate values
5. Copy the code and paste it into the `pyspark` shell

## [Next »](../04_Glue_Crawler/README.md)
