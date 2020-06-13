import os
import json
import boto3

ses_client = boto3.client('ses')

def lambda_handler(event, context):

  print(event)


#   try:
#     publish_sns_update(text_message)
#     print("Message send success.")
#   except Exception as error:
#     print(f"Message send failed, error: {error}")

# def publish_sns_update(text_message):

#   response = sns_client.publish(
#       TargetArn = os.environ['SNS_TOPIC_ARN'], 
#       Message=json.dumps({'default': text_message}),
#       MessageStructure='json'
#   )

#   return response