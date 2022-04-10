from django.contrib.auth.models import User
from django.db import models


class UserSignUpDateInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="signup_date_info")
    info = models.JSONField(null=True)
