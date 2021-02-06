# receive-ses-email

1. Email is sent to an SES domain.

2. Email content is stored as an S3 file.

3. An SNS notification is sent, triggering a Lambda function.

4. The function takes the S3 file details, extracts the message, and attemps to categorize the email type.

5. The function then sends an email through SES to the user notifying them of the email.