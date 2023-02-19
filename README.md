# AWS Cloud Formation Lambda Backed Custom Resource Example

## What does this do? 

- Uses a lambda backed custom resource to provision Redis cluster with preset configuration and automatically seed data into the cluster
- This would be useful if you want to deploy a custom resource, in this example Redis clusters in multiple AWS environments such as production and test using Cloud Formation templates with the same customizations and exact copies of the data seeded on each cluster

## Things to consider 

- Don't hardcode passwords for the cluster, fetch these from AWS Secrets Manager instead 
- You can also use Terraform, with the CloudFormation template body inline and call the Lambda ARN
