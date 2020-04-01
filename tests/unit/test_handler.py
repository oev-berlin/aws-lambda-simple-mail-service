import json
import boto3
import pytest

from moto import mock_ses
from mail_service import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
   "resource":"/send_mail",
   "path":"/send_mail",
   "httpMethod":"POST",
   "headers":{
      "Accept":"*/*",
      "Accept-Encoding":"gzip, deflate, br",
      "Accept-Language":"en-US,en;q=0.9",
      "CloudFront-Forwarded-Proto":"https",
      "CloudFront-Is-Desktop-Viewer":"true",
      "CloudFront-Is-Mobile-Viewer":"false",
      "CloudFront-Is-SmartTV-Viewer":"false",
      "CloudFront-Is-Tablet-Viewer":"false",
      "CloudFront-Viewer-Country":"DE",
      "content-type":"application/json",
      "Host":"sx45sckuq3.execute-api.eu-central-1.amazonaws.com",
      "origin":"http://localhost:3000",
      "Referer":"https://sx45sckuq3.execute-api.eu-central-1.amazonaws.com/",
      "sec-fetch-dest":"empty",
      "sec-fetch-mode":"cors",
      "sec-fetch-site":"cross-site",
      "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
      "Via":"2.0 a477b8537c9bc4c10a3c144386a7b5bf.cloudfront.net (CloudFront)",
      "X-Amz-Cf-Id":"RpmxBCGzn7mxKaMtdWznn9pUigmknv0PhOCgh7QlozhKBsBmpIIkqA==",
      "X-Amzn-Trace-Id":"Root=1-5e849096-f37b0f44aa32431c48351458",
      "X-Forwarded-For":"84.160.92.244, 70.132.42.154",
      "X-Forwarded-Port":"443",
      "X-Forwarded-Proto":"https"
   },
   "multiValueHeaders":{
      "Accept":[
         "*/*"
      ],
      "Accept-Encoding":[
         "gzip, deflate, br"
      ],
      "Accept-Language":[
         "en-US,en;q=0.9"
      ],
      "CloudFront-Forwarded-Proto":[
         "https"
      ],
      "CloudFront-Is-Desktop-Viewer":[
         "true"
      ],
      "CloudFront-Is-Mobile-Viewer":[
         "false"
      ],
      "CloudFront-Is-SmartTV-Viewer":[
         "false"
      ],
      "CloudFront-Is-Tablet-Viewer":[
         "false"
      ],
      "CloudFront-Viewer-Country":[
         "DE"
      ],
      "content-type":[
         "application/json"
      ],
      "Host":[
         "sx45sckuq3.execute-api.eu-central-1.amazonaws.com"
      ],
      "origin":[
         "http://localhost:3000"
      ],
      "Referer":[
         "https://sx45sckuq3.execute-api.eu-central-1.amazonaws.com/"
      ],
      "sec-fetch-dest":[
         "empty"
      ],
      "sec-fetch-mode":[
         "cors"
      ],
      "sec-fetch-site":[
         "cross-site"
      ],
      "User-Agent":[
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
      ],
      "Via":[
         "2.0 a477b8537c9bc4c10a3c144386a7b5bf.cloudfront.net (CloudFront)"
      ],
      "X-Amz-Cf-Id":[
         "RpmxBCGzn7mxKaMtdWznn9pUigmknv0PhOCgh7QlozhKBsBmpIIkqA=="
      ],
      "X-Amzn-Trace-Id":[
         "Root=1-5e849096-f37b0f44aa32431c48351458"
      ],
      "X-Forwarded-For":[
         "84.160.92.244, 70.132.42.154"
      ],
      "X-Forwarded-Port":[
         "443"
      ],
      "X-Forwarded-Proto":[
         "https"
      ]
   },
   "queryStringParameters":"None",
   "multiValueQueryStringParameters":"None",
   "pathParameters":"None",
   "stageVariables":"None",
   "requestContext":{
      "resourceId":"8z5c8t",
      "resourcePath":"/send_mail",
      "httpMethod":"POST",
      "extendedRequestId":"KTuHgFoYliAFfKg=",
      "requestTime":"01/Apr/2020:13:01:10 +0000",
      "path":"/Prod/send_mail",
      "accountId":"326094939662",
      "protocol":"HTTP/1.1",
      "stage":"Prod",
      "domainPrefix":"sx45sckuq3",
      "requestTimeEpoch":1585746070353,
      "requestId":"5f424695-f4d3-4d7a-b141-e2d2b308e630",
      "identity":{
         "cognitoIdentityPoolId":"None",
         "accountId":"None",
         "cognitoIdentityId":"None",
         "caller":"None",
         "sourceIp":"84.160.92.244",
         "principalOrgId":"None",
         "accessKey":"None",
         "cognitoAuthenticationType":"None",
         "cognitoAuthenticationProvider":"None",
         "userArn":"None",
         "userAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
         "user":"None"
      },
      "domainName":"sx45sckuq3.execute-api.eu-central-1.amazonaws.com",
      "apiId":"sx45sckuq3"
   },
   "body":"{\"gender\":\"female\",\"name\":\"Mercedes Noel\",\"date\":\"1997-01-16\",\"place\":\"18\",\"space\":\"46\",\"isInsured\":\"yes\",\"email\":\"zaraz@mailinator.com\",\"telNumber\":\"397\"}",
   "isBase64Encoded":False
}

@pytest.fixture()
def mocker():
    return ""

def create_mock_ses_client():
    ses = boto3.client('ses')
    ses.verify_email_identity(EmailAddress="no-reply@45plus.oev-berlin.de")
    
    return ses

@mock_ses
def test_send_mail():

    create_mock_ses_client()

    response = app.send_mail("jhornung@oev.de", "Test")
    assert "MessageId" in response

@mock_ses
def test_lambda_handler(apigw_event, mocker):

    create_mock_ses_client()    

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])
    assert data["ResponseMetadata"]["HTTPStatusCode"] == 200
