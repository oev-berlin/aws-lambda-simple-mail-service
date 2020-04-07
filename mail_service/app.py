import json
import boto3

def send_mail(destination, message):
    """ sends an e-mail using SES with the given parameters """
    
    ses = boto3.client('ses')
    response = ses.send_email(
        Source='no-reply@45plus.oev-berlin.de',
        Destination={
            'ToAddresses': [
                destination,
            ]
        },
        Message={
            'Subject': {
                'Data': 'Betreff 45plus'
            },
            'Body': {
                'Text': {
                    'Data': message
                }
            }
        }
    )
    return response


def lambda_handler(event, context):
    """Sample pure Lambda function """
    
    data = json.loads(event['body'])
    destination = data['email']
    try:
        message = data['message']
    except:
        message = "no message set"


    response = send_mail(destination, message)

    return {
        "statusCode": 200,
        "body": json.dumps(response),
        "headers": { 
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Credentials' : True,
            'Content-Type': 'application/json'
        },
    }
