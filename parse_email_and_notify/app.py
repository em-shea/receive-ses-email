import os
import json
import boto3

s3 = boto3.resource('s3')
sns_client = boto3.client('sns', region_name=os.environ['AWS_REGION'])
ses_client = boto3.client('ses', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):

  bucket_key = event['Records'][0]['s3']['object']['key']
  bucket_name = event['Records'][0]['s3']['bucket']['name']
  bucket_region = event['Records'][0]['awsRegion']

  obj = s3.Object(bucket_name, bucket_key)
  obj_content_string = obj.get()['Body'].read().decode('utf-8')

  content_type, notification_message = parse_email_obj(obj_content_string)

  link_to_file = "https://s3.console.aws.amazon.com/s3/object/" + bucket_name + "?region=" + bucket_region + "&prefix=" + bucket_key

  notification_email_content = get_notification_template(content_type, notification_message, link_to_file)

  try:
    send_notification_email(content_type, notification_email_content)
    print("Message send success.")
  except Exception as error:
    print(f"Message send failed, error: {error}")

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
    notification_message = initial_string.split(";")[0].strip()[0:5]
  elif "MIME-Version: 1.0" in obj_content_string:
    content_type = "inbound message"
    notification_message = obj_content_string.split("MIME-Version: 1.0")[1]
  else:
    content_type = "uncategorized email type"
    notification_message = "See S3 file link for message details."
  
  print('content_type: ', content_type)
  print('notif: ', notification_message)

  return content_type, notification_message

def get_notification_template(content_type, notification_message, link_to_file):

  # To run unit tests for this function, we need to specify an absolute file path
  abs_dir = os.path.dirname(os.path.abspath(__file__))
  with open(os.path.join(abs_dir, 'notification_email_template.html')) as fh:
      contents = fh.read()

  notification_email_contents = contents.replace("{content_type}", content_type)
  notification_email_contents = notification_email_contents.replace("{notification_message}", notification_message)
  notification_email_contents = notification_email_contents.replace("{link_to_file}", link_to_file)

  return notification_email_contents

def send_notification_email(content_type, notification_email_content):

    response = ses_client.send_email(
        Source = "Email received notification <emailreceived@" + os.environ['EMAIL_DOMAIN'] + ">",
        Destination = {
            "ToAddresses" : [
            os.environ['EMAIL_ADDRESS']
            ]
        },
        Message = {
            "Subject": {
            "Charset": "UTF-8",
            "Data": "Email received - " + content_type
            },
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": notification_email_content
                }
            }
        }
    )

    return response