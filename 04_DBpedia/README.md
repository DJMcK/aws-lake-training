# DBpedia Data

Here we will source a dataset that is already well groomed directly into our "landing" bucket. From there we will further refine the dataset to optimize for querying with Amazon Athena.

In other words, we will take several CSV files (`train.csv` and `test.csv`) and ETL to a single Parquet source that is partitioned by the test & train category.

## Land Data

```bash
aws s3 cp train.csv.gz s3://$STACK_NAME-landing/dbpedia/
aws s3 cp test.csv.gz s3://$STACK_NAME-landing/dbpedia/
```

## Refine Data

1. Connect to your EMR Cluster (as described in [04_EMR_Cluster](../02_EMR_Cluster/README.md))
2. Run `pyspark`
3. Open [`dbpedia.curate.py`](./dbpedia.curate.py) in an editor
4. Update the values for `BUCKET_LANDING` and `BUCKET_CURATED` with the appropriate values
5. Copy the code and paste it into the `pyspark` shell

## [Next »](../05_Terminate_EMR_Cluster/README.md)
