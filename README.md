# receive-ses-email

This is app receives and parses inbound emails to your SES domain. It then sends a notification message to your personal email with details about the email contents.

### How it works:

1. Email is sent to an SES domain. 📨

2. Email content is stored as an S3 file, triggering a Lambda function. ⚡

3. The function takes the S3 file details, extracts the message, and attemps to categorize the email type. 🤔

4. The function then sends an email through SES to the user notifying them of the email. 📬

### How to get started:

- Verify your SES email domain - [Docs](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domain-procedure.html)
- Set up three environment variables. I'm using CircleCI to [store my environment variables](https://circleci.com/docs/2.0/env-vars/#setting-an-environment-variable-in-a-project) and deploy the app.
    - `EMAIL_BUCKET_NAME` - Choose a name for the S3 bucket that will be created to store email files. Make sure this is globally unique. Ex, my-bucket-name-02-06 
    - `EMAIL_DOMAIN` - The verified SES domain name that the notification emails will be sent from. I'm using the same domain to send notifications as the one this app parses emails for, but this can be any verified SES domain. Ex, mydomain.com
    - `EMAIL_ADDRESS` - The email address that will receive notifications when a new email is sent to your SES domain. Ex, myemail@gmail.com
- Once you've deployed this CloudFormation stack, set up an SES rule to save inbound email message files to the S3 bucket that was created - [Docs](https://aws.amazon.com/premiumsupport/knowledge-center/ses-receive-inbound-emails/)

If you're new to deploying serverless applications through a deployment pipeline, check out this intro [blog post](https://emshea.com/post/serverless-cicd).