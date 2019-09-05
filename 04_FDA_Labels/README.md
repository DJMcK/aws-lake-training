# FDA Drug Labels Data

The FDA provides a wealth of large data sets via the [OpenFDA](https://open.fda.gov/) website and APIs. We will leverage one of these data sets in particiular; the [Drug Labels](https://open.fda.gov/apis/drug/label/).

## Raw Data

The FDA provides access to all of the [OpenFDA](https://open.fda.gov/) data via a public S3 bucket. We can pull this data in directly using the following command:

```bash
aws s3 sync s3://download.open.fda.gov/2019-08-10/drug/label s3://$STACK_NAME-raw/fda/2019-08-10/drug/label
```

> **Note:** The above command assumes that you have the `STACK_NAME` variable set in your terminal from our setup steps.

## Land Data

In order to land the data, we will be using an EMR Cluster with a very large EC2 instance type.

> **Note:** As part of the training, the instructor will perform this phase to show how to use EMR and expose the landed data set.

**Objectives for this section:**

1. Take the raw `zip` "parts" as an input
2. `deflate` the files and save as `gzip` compressed `json` files - this puts them in a format we can interact with using Spark
3. Read the compressed `json` files as a [DataFrame](https://spark.apache.org/docs/2.2.0/sql-programming-guide.html#datasets-and-dataframes)
4. Select the property we want to extract from the large object
5. `explode` the list of results creating a new structure where each drug is now a row
6. Land the new optimized data set as `gzip` compressed `json` files

**The instructor will demonstrate:**

1. Creating an EMR Cluster
2. Connecting using SSH
3. Running the Spark Shell (in our case [`pyspark`](https://spark.apache.org/docs/latest/api/python/index.html))
4. Executing the code in [`fda.01.land.py`](./fda.01.land.py) to achieve our above objectives for this stage
5. Provide the class with access to the landed date and command to sync this to their "landing" buckets

## Curate Data

> **Prerequisite:** The output from the [Land Data](#land-data) should be in your "landing" bucket ready for curation.

1. Connect to your EMR Cluster (as described in [04_EMR_Cluster](../04_EMR_Cluster/README.md))
2. Run `pyspark`
3. Open [`fda.02.curate.py`](./fda.02.curate.py) in an editor
4. Update the values for `BUCKET_LANDING` and `BUCKET_CURATED` with the appropriate values
5. Copy the code and paste it into the `pyspark` shell

## Ehance Data

1. Connect to your EMR Cluster (as described in [04_EMR_Cluster](../04_EMR_Cluster/README.md))
2. Run `pyspark`
3. Open [`fda.03.enhance.py`](./fda.03.enhance.py) in an editor
4. Copy the code and paste it into the `pyspark` shell

## [Next »](../05_DBpedia/README.md)
