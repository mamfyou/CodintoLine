from random import randint

from celery import shared_task
import os

from dotenv import dotenv_values

from core.models import Token
from melipayamak import Api


@shared_task
def send_sms(to, user):
    username = dotenv_values(".env")['SMS_USERNAME']
    password = dotenv_values(".env")['SMS_PASSWORD']
    api = Api(username, password)
    sms = api.sms()
    to = to
    _from = dotenv_values(".env")['SMS_HOST']
    token = Token.objects.create(user_id=user, token=randint(100000, 999999))
    text = 'کد تایید شما: ' + str(token.token)
    response = sms.send(to, _from, text)
    print(response)
    return response
