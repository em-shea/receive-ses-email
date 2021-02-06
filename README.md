# receive-ses-email 📬

This app receives and parses inbound emails to your SES domain. It then sends a notification message to your personal email with details about the email contents.

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

If you're new to deploying serverless applications using a deployment pipeline, check out this intro [blog post](https://emshea.com/post/serverless-cicd).

#### Example notification email

![Example notification email](https://emshea-static.s3.amazonaws.com/example-notification.png)

### Email types

The categorization of what type an incoming email is loosely based on features of the email content string and definitely not 100% accurate. I've created four categories based on emails I've received to my SES domain so far and will add more as I get new types.
1. **delivery failure (bad email)** - This is a bounce back message received when your SES domain tries to send a message to an email that is not valid.
2. **delivery error (bot)** - This is a bounce back message from seemingly bot traffic.
3. **inbound message** - This is a normal email message sent to your SES domain.
4. **uncategorized email type** - This is a catch all type for emails that are not the three types above.

If you come across any others that you would like supported, feel free to submit a pull request.