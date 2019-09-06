# Comprehend Medical Serverless Workflow Repository

## Architecture

![alt text](images/architecture.png "Logo Title Text 1")

## Outline
1. Build demo lambda function
2. Why use a framework such as Serverless or SAM?
3. Quick overview of Comprehend Medical interface
4. Comprehend Medical pipeline demo

## Setup
#### Create bucket in S3
* Create bucket using the cloudformation script. 
* *IMPORTANT: Replace bucket name in the commented part.*
* Create folders:
    * athenaoutput
    * comprehendoutput
    * uploadsfolder

#### Clone repository
* *IMPORTANT: Replace bucket name in serverless.yml to your bucket.*
* *IMPORTANT: Change DynamoDB table name.*

#### Install Serverless Framework
* Install nodejs from https://nodejs.org/en/download/
* **We need to set the proxy to do an npm install of the serverless framework. Please run the 2 commands attached in your email with subject 'npm config set' before proceeding**

* Install serverless framework
    ```
    npm install -g serverless
    ```
* Check serverless version 
    ```
    serverless --version
    ```

Reference: https://serverless.com/framework/docs/providers/aws/guide/installation/

#### Plugins
* change directory to comprehend-service folder in your terminal.
* install following plugins
```
npm install --save-dev serverless-step-functions

npm install serverless-pseudo-parameters
```

#### Deploy
```
serverless deploy --verbose --force
```

#### Notes:

###### Demo Lambda
Numpy layer
arn:aws:lambda:us-east-2:874346574520:layer:pandas-xlrd-layer-Python36-Pandas23x:5

###### Serverless - npm config
check email