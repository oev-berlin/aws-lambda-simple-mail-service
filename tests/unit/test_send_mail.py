import json
import pytest
import boto3
from moto import mock_ses

import mail_service.app as handler

@mock_ses
def test_send_mail():   

    response = handler.send_mail("jhornung@oev.de", "Test")
    print(response)
    assert "MessageId" in response
    return "s"
