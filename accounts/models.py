from django.db import models
from django.contrib.auth.models import AbstractUser
from StackOfMusic import settings


class User(AbstractUser):
    GENDER_MAIL, GENDER_FEMAIL = 0, 1
    GENDER_OPTION = (
        (GENDER_MAIL, '남성'),
        (GENDER_FEMAIL, '여성'),
    )
    sex = models.SmallIntegerField(choices=GENDER_OPTION, null=True)
    age = models.IntegerField(default=0)
    bank_account_number = models.CharField(max_length=15)
    bank = models.OneToOneField('bank.Bank', on_delete=models.CASCADE, related_name='bank', null=True)

    class Meta:
        swappable = settings.AUTH_USER_MODEL
