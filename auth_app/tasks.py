import datetime
import json

import requests
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User

from .models import UserSignUpDateInfo


@shared_task
def save_user_sign_up_date_info(user_id):
    user = User.objects.filter(id=user_id).first()
    if user:
        ip_info_url = f"{settings.IP_INFO_URL}/?api_key={settings.IP_API_KEY}"
        response = requests.get(ip_info_url)
        response_body = json.loads(response.content)
        country_code = response_body["country_code"]
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        day = today.day
        holiday_info_url = f"{settings.HOLIDAY_INFO_URL}/" \
                           f"?api_key={settings.HOLIDAYS_API_KEY}" \
                           f"&country={country_code}&year={year}&month={month}&day={day}"
        response = requests.get(holiday_info_url)
        response_body = json.loads(response.content)

        UserSignUpDateInfo.objects.create(user=user, info=response_body)
