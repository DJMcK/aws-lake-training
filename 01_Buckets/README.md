# Lake Buckets

In this section, we're going to spin up some AWS S3 Buckets for all of our source data and artifacts. To do this, we're also going to introduce AWS CloudFormation as our deployment mechanism.

## Lake Name

Before deploying anything, first we give our lake a unique name:

**Bash:**

```bash
export STACK_NAME="<NAME>"
```

> **Windows:** `set STACK_NAME="<NAME>"`

## Deploy: Artifacts Bucket

The artifacts buckets is used to store deployment artifacts (compiled code, cloudformation templates, etc.)

To deploy this bucket, run the following command:

```bash
sam deploy --template-file ./deployment-artifacts.yaml --stack-name $STACK_NAME-deployment-artifacts
```
> **Windows:** `sam deploy --template-file ./deployment-artifacts.yaml --stack-name %STACK_NAME%-deployment-artifacts`

## Deploy: Lake Buckets

This step will deploy a total of three buckets to AWS. This includes:

* **Raw** - used to store data in a very raw format (binary data, zip archives, etc) with very short time-to-live (TTL) before data is archived using AWS Glacier
* **Landing** - used to store data that may be non-optimal in its storage format or require transformation before becoming useful
* **Curated** - used to store data that has gone through any necessary ETL processes and is accessible for lake users

To deploy the lake buckets, run:

```bash
sam deploy --template-file ./lake-buckets.yaml --stack-name $STACK_NAME
```
> **Windows:** `sam deploy --template-file ./lake-buckets.yaml --stack-name %STACK_NAME%`

## [Next »](../02_EMR_Cluster/README.md)
