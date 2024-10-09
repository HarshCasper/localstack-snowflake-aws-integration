#!/bin/bash

export AWS_ENDPOINT_URL=http://localhost:4666

awslocal s3 mb s3://testbucket

awslocal s3 cp /etc/localstack/init/main.py s3://testbucket/

awslocal emr create-cluster \
    --name "emr-snowflake-cluster" \
    --release-label emr-6.8.0 \
    --applications Name=Spark \
    --instance-type m5.xlarge \
    --instance-count 1

CLUSTER_ID=$(awslocal emr list-clusters --active --query 'Clusters[?Name==`emr-snowflake-cluster`].Id' --output text)

awslocal emr add-steps --cluster-id $CLUSTER_ID --steps '[
  {
    "Name": "Snowflake Python Step",
    "ActionOnFailure": "CONTINUE",
    "Type": "CUSTOM_JAR",
    "Jar": "command-runner.jar",
    "Args": [
      "bash", "-c",
      "pip3 install snowflake-connector-python[pandas] && awslocal --endpoint-url http://localhost:4666 s3 cp s3://testbucket/main.py /tmp/main.py && python3 /tmp/main.py"
    ]
  }
]'
