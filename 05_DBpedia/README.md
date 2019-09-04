## Land Data in S3 Bucket

```bash
aws s3 cp train.csv.gz s3://$STACK_NAME-landing/dbpedia/
aws s3 cp test.csv.gz s3://$STACK_NAME-landing/dbpedia/
```
