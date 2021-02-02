import os
import json
import boto3

s3 = boto3.resource('s3')
sns_client = boto3.client('sns')

def lambda_handler(event, context):

  print('event: ', event)

  bucket_key = event['Records'][0]['s3']['object']['key']
  bucket_name = event['Records'][0]['s3']['bucket']['name']
  bucket_region = event['Records'][0]['awsRegion']

  obj = s3.Object(bucket_name, bucket_key)
  obj_content_string = obj.get()['Body'].read().decode('utf-8')

  content_type, notification_message = parse_email_obj(obj_content_string)

  link_to_file = "https://s3.console.aws.amazon.com/s3/object/" + bucket_key + "?region=" + bucket_region "&prefix=" + bucket_name

  print('link: ', link_to_file)
  # print('content_type: ', content_type)
  # print('notif: ', notification_message)

  # print('type: ', type(obj_content_string))

  # print('obj_content_string: ', obj_content_string)

  # email_content = event['Records'][0]['ses']['mail']['commonHeaders']

  # print(email_content)

  # try:
  #   publish_sns_update(email_content)
  #   print("Message send success.")
  # except Exception as error:
  #   print(f"Message send failed, error: {error}")

def parse_email_obj(obj_content_string):
  
  content_type = "none"
  notification_message = "empty"

  if "Delivery Status Notification (Failure)" in obj_content_string:
    content_type = "delivery failure (bad email)"
    initial_string = obj_content_string.split("An error occurred while trying to deliver the mail to the following recipients:",1)[1]
    notification_message = initial_string.split("------=_Part_")[0].strip()
  elif "Delivery error report" in obj_content_string:
    content_type = "delivery error (bot)"
    initial_string = obj_content_string.split("envelope-from=",1)[1]
    notification_message = initial_string.split(";")[0].strip()
  else:
    content_type = "inbound message"
    notification_message = obj_content_string.split("MIME-Version: 1.0")[1]
  
  print('content_type: ', content_type)
  print('notif: ', notification_message)

  return content_type, notification_message

def publish_sns_update(email_content):

  content_string = json.dumps(email_content)

  email_body = ""

  response = sns_client.publish(
      TargetArn = os.environ['SNS_TOPIC_ARN'], 
      Message=json.dumps({'default': content_string}),
      MessageStructure='json'
  )

  return response