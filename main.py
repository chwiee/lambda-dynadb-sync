import os
import json
import boto3

def lambda_handler(event, context):
  TARGET_AWS_ACCOUNT      = ""
  TARGET_ROLE_NAME        = ""
  TARGET_DDB_NAME         = ""
  TARGET_DDB_REGION       = ""
  role_rn                 = f"arn:aws:iam::{TARGET_AWS_ACCOUNT}:role/{TARGET_ROLE_NAME}"
  res                     = get_credentials(role_rn)
  ddb                     = boto3.client('dynamodb', region_name  = TARGET_DDB_REGION,
                                          aws_access_key_id       = res['AccessKeyId'],
                                          aws_secret_access_key   = res['SecretAccessKey'],
                                          aws_session_token       = res['SessionToken'])

  records                 = event['Records']

  for record in records:
    event_name  = record['eventName']
    print(record)

    if event_name == 'REMOVE':
      ret = dynamodb.delete_item(TableName=TARGET_DDB_NAME, Key=record['dynamodb']['Keys'])
      print(f'Removing: {record['dynamodb']['Keys']}')
    else:
      ret = dyanmodb.put_item(TableName=TARGET_DDB_NAME, Item=record['dynamodb']['NewImage'])
      print(f'Put new item: {record['dynamodb']['NewImage']}')

def get_credentials(role_arn):
  client              = boto3.client('sts')
  assumed_role_object = client.assume_role(
    RoleArn           = role_arn,
    RoleSessionName   = 'cross_acct_lambda'
  )

  client_res  = assumed_role_object['Credentials']
  return client_res
