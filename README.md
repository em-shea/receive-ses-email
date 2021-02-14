# receive-ses-email 📬

**This is a serverless app that receives and parses inbound emails sent to your Amazon Simple Email Service (SES) domain. It then sends a notification message to your personal email with details about the email contents.**

For some background on this app, I wanted to find a way to handle inbound emails being sent to an SES domain for a project of mine, [Haohaotiantian](haohaotiantian.com). Haohaotiantian sends out daily emails to its subscribers from an SES email. I often receive bounce backs when people sign up to the service with a misspelled or otherwise invalid email.

When I searched for how to handle inbound emails, all of the tutorials that I could find were just for the first step - [automatically storing inbound emails in S3](https://aws.amazon.com/premiumsupport/knowledge-center/ses-receive-inbound-emails/). I set up an SNS notification to let me know when a new email was saved in S3, but I still needed to go to S3 and download the object to see what was in the email. This app automates the second step, providing you with a preview of what type of email message you have received and (if it's a regular inbound email and not an error message) the email content.

## How it works:

1. Email is sent to your SES domain. 📨

2. The email content is stored as an S3 object, triggering a Lambda function. ⚡

3. The function gets the S3 object, reads the email content, and attemps to categorize what type of email it is. 🤔

4. The function then sends a notification email through SES to your personal email. 📬

## How to get started:

- Verify your SES email domain - [Docs](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domain-procedure.html)
- Create two S3 buckets:
    - The first bucket will store the CloudFormation template that SAM generates.
    - The second bucket will store the inbound email files.
- Set up four environment variables. I'm using CircleCI to [store my environment variables](https://circleci.com/docs/2.0/env-vars/#setting-an-environment-variable-in-a-project) and deploy the app.
    - `SAM_BUCKET` - The name of the S3 bucket where the SAM-generated CloudFormation template is stored.
    - `EMAIL_BUCKET_NAME` - The name of the S3 bucket where inbound email files are stored.
    - `EMAIL_DOMAIN` - The verified SES domain name that the notification emails will be sent from. I'm using the same domain to send notifications as the one this app receives inbound emails for, but you can use any verified SES domain here. Ex, mydomain.com. Your SES domain will need to be [out of sandbox mode in order to send emails](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html?icmpid=docs_ses_console).
    - `EMAIL_ADDRESS` - The personal email address that will receive notifications when a new email is sent to your SES domain. Ex, myemail@gmail.com
- Once you've deployed this CloudFormation stack, set up an SES rule to save inbound email messages to the S3 bucket that was created - [Docs](https://aws.amazon.com/premiumsupport/knowledge-center/ses-receive-inbound-emails/)

If you're new to deploying serverless applications using a deployment pipeline, check out this intro [blog post](https://emshea.com/post/serverless-cicd).

### Example notification email

![Example notification email](https://emshea-static.s3.amazonaws.com/notification.png)

## Email types

The categorization of what type an incoming email is loosely based on features of the email content string and definitely not 100% accurate. I've created four categories based on emails I've received to my SES domain so far and will add more as I get new types.
1. **delivery failure (bad email)** - This is a bounce back message received when your SES domain tries to send a message to an email that is not valid.
2. **delivery error (bot)** - This is a bounce back message from what seems like inbound bot traffic.
3. **inbound message** - This is a normal email message sent to your SES domain.
4. **uncategorized email type** - This is a catch all type for emails that are not the three types above.

If you come across any others that you would like supported, feel free to submit a pull request.