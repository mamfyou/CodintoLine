from random import randint

from celery import shared_task
from dotenv import dotenv_values

from core.models import Token
from melipayamak.sms import Rest

@shared_task
def send_sms(to, user):
    username = dotenv_values(".env")['SMS_USERNAME']
    password = dotenv_values(".env")['SMS_PASSWORD']
    api = Rest(username, password)
    _from = dotenv_values(".env")['SMS_HOST']
    token = Token.objects.create(user_id=user, token=randint(100000, 999999))
    text = str(token.token)
    response = sms = api.send_by_base_number(to=to, text=text, bodyId=120794)
    print(response)
    return response
