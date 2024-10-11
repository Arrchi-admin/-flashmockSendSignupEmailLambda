import boto3
import json

ses = boto3.client('ses', region_name='us-west-2')  # Replace 'your-region' with the region you are using

# Function to send email
def  send_email(recipient_email, subject, body_html):
    sender_email = "chidvi@flashmock.com"  # Replace with your sender email
    print(recipient_email, subject,body_html )

    try:
        response = ses.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [recipient_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        print("Email Send Response")
        print(response)
        return response
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {'error': str(e)}


# Lambda handler function
def lambda_handler(event, context):
    try:
        # Extract query parameters
        query_params = event.get('queryStringParameters', {})
        recipient_email = query_params.get('email', '')
        user_name = query_params.get('name', 'User')  # Default to 'User' if no name is provided
        referral_link = query_params.get('referral_link', 'https://www.flashmock.com')  # Default referral link
        share_message = query_params.get('share_message', 'I just earned 10 free mock interviews with FlashMock! Join me and get your own free mock interviews. Use my referral link:')

        # Check if email is provided
        if not recipient_email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Email is required'})
            }

        # Define email subject and body
        subject = "Welcome to FlashMock! You’ve Earned 5 Free Mock Interviews 🎉"

        # Replace name, referral link, and share message dynamically in the email body
        body_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to FlashMock</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .logo {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .logo img {{
            max-width: 150px;
            height: auto;
        }}
        h1 {{
            color: #FF7F50;
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .highlight {{
            background-color: #FF7F50;
            color: #ffffff;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .button-container {{
            text-align: center;
            margin-top: 30px;
            color: #ffffff;
        }}
        .button {{
            display: inline-block;
            background-color: #FF7F50;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        }}
        .button:hover {{
            background-color: #E76642;
        }}
        .link {{
            color: #FF7F50;
            text-decoration: none;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="https://www.flashmock.com/assets/FlashMockLogoFullCoralOrange-BY4-2L4i.png" alt="FlashMock Logo">
        </div>

        <p>Hi {user_name},</p>

        <p>Congratulations! You've earned <span class="highlight">10 free mock interviews</span> to kickstart your journey toward interview success.</p>

        <p>We're thrilled to have you on board as one of our early adopters.</p>
        <p>The beta will be live on <strong>November 1st</strong>. We'll notify you by email when it's ready!</p>

        <p>Want more mock interviews? Refer your friends! When a friend signs up, both of you receive an additional free mock interview.</p>

        <div class="button-container">
            <a href="{referral_link}" target="_blank" class="button">Open Your Referral Link</a>
           </div>

        <p>Log in anytime to access your referral link: <a href="https://www.flashmock.com" class="link">https://www.flashmock.com</a></p>
    </div>
</body>
</html>
        """

        # Send the email
        response = send_email(recipient_email, subject, body_html)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent successfully', 'response': response})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
