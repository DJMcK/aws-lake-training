# AWS Athena - Data Access

Now that you're data has been refined and crawled, it is now accessible via [AWS Athena](https://aws.amazon.com/athena/).

> **What is Athena?**
>
> Athena provides you the capability to query your data sitting on S3 using a SQL interface. It is completely serverless making it easy to manage and pay-per-use (query). The efficiency of Athena is largely dependent on the structure and storage format of your data. This is why we performed some pre-work to optimize exactly that storing our data in a columnar optimized storage format (Parquet).

## Creating Views

Now that we have the FDA dataset accessible to us via Athena, we'll want to create some views of that data help us derive useful insights.

We can do this by:

1. Go to the [AWS Athena Dashboard](https://us-east-2.console.aws.amazon.com/athena/home?region=us-east-2#query)
2. Run each query from below individually (remember to replace `<YOUR_DATABASE>` from each query)

**Product Routes:**
```sql
CREATE OR REPLACE VIEW product_labels_routes AS
SELECT id, LOWER(routes) as routes, effective_date FROM "<YOUR_DATABASE>"."fda_product"
CROSS JOIN UNNEST(openfda.route) as t(routes);
```

**Product Substance Names:**
```sql
CREATE OR REPLACE VIEW product_labels_substances AS
SELECT id, LOWER(substances) as substances, effective_date FROM "<YOUR_DATABASE>"."fda_product"
CROSS JOIN UNNEST(openfda.substance_name) as t(substances);
```

**Product Manufacturer Names:**
```sql
CREATE OR REPLACE VIEW product_labels_manufacturers AS
SELECT id, LOWER(manufacturers) as manufacturers, effective_date FROM "<YOUR_DATABASE>"."fda_product"
CROSS JOIN UNNEST(openfda.manufacturer_name) as t(manufacturers);
```

**Product Indications:**
```sql
CREATE OR REPLACE VIEW product_labels_indications AS
SELECT id, LOWER(indications) as indications, effective_date FROM "<YOUR_DATABASE>"."fda_product"
CROSS JOIN UNNEST(extracted_text) as t(indications);
```

> **Tip:** Each of these queries is essentially taking a column which contains an array of strings and unnesting those arrays into individual columns.
