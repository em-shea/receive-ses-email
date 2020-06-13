import os
import json
import boto3

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

def lambda_handler(event, context):

  print(event)

  object_key = event[0]['s3']['object']['key']

  bucket_name = os.environ['S3_BUCKET_NAME']

  obj = s3_client.Object(bucket_name, object_key)
  email_string = obj.get()['Body'].read().decode('utf-8') 

  print(email_string)

  # email_content = event['Records'][0]['ses']['mail']['commonHeaders']

  # print(email_content)

  # try:
  #   publish_sns_update(email_content)
  #   print("Message send success.")
  # except Exception as error:
  #   print(f"Message send failed, error: {error}")

def publish_sns_update(email_content):

  content_string = json.dumps(email_content)

  email_body = ""

  response = sns_client.publish(
      TargetArn = os.environ['SNS_TOPIC_ARN'], 
      Message=json.dumps({'default': content_string}),
      MessageStructure='json'
  )

  return response