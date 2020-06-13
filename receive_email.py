import os
import json
import boto3

sns_client = boto3.client('sns')

def lambda_handler(event, context):

  email_content = event['Records'][0]['ses']['mail']['commonHeaders']

  print(email_content)

  try:
    publish_sns_update(email_content)
    print("Message send success.")
  except Exception as error:
    print(f"Message send failed, error: {error}")

def publish_sns_update(email_content):

  response = sns_client.publish(
      TargetArn = os.environ['SNS_TOPIC_ARN'], 
      Message=json.dumps({'default': email_content}),
      MessageStructure='json'
  )

  return response