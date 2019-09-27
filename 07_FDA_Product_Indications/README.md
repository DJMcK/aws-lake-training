# FDA Product Indications

Now that we have some new information sitting in our "landing" bucket, we'll want to combine that information with our existing FDA Product Labels data. For that, we can go back to our EMR cluster to help facilitate that MapReduce task.

## Combine Products & Extracted Indications

Using our EMR cluster, we'll load both our FDA Product Labels data and our indications extraction data. Using the shared ID field as a key, we'll then be able to join the data together and save that information back to the "curated" bucket ready for consumption.

1. Connect to your EMR Cluster (as described in [02_EMR_Cluster](../02_EMR_Cluster/README.md))
2. Run `pyspark`
3. Open [`fda.indications.py`](./fda.indications.py) in an editor
4. Update the values for `BUCKET_LANDING` and `BUCKET_CURATED` with the appropriate values
5. Copy the code and paste it into the `pyspark` shell

## Run the Crawler

Given that we have just updated the FDA Product Labels data with a new column, what that means is our data's schema has now changed. We can easily update our Athena tables by rerunning our Glue Crawler.

1. From the [AWS Glue Crawler Dashboard](https://us-east-1.console.aws.amazon.com/glue/home?region=us-east-1#catalog:tab=crawlers)
2. Click on your newly created Crawler
3. Click "Run crawler"

## Create the Athena View

1. Go to the [AWS Athena Dashboard](https://us-east-1.console.aws.amazon.com/athena/home?region=us-east-1#query)
2. Run each query from below (remember to replace `<YOUR_DATABASE>`)

**Product Indications:**
```sql
CREATE OR REPLACE VIEW product_labels_indications AS
SELECT id, LOWER(indications) as indications, effective_date FROM "<YOUR_DATABASE>"."<YOUR_TABLE>"
CROSS JOIN UNNEST(extracted_text) as t(indications);
```

## [Next »](../08_Terminate_EMR_Cluster/README.md)
