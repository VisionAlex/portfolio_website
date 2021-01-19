from django.db import models
from django.contrib.auth.models import AbstractUser

CURRENCIES = (
    ('EUR', 'EUR'),
    ('GBP', 'GBP'),
    ('USD', 'USD'),
)

class CustomUser(AbstractUser):
    currency = models.CharField("Main Currency", max_length=3, default="EUR", choices=CURRENCIES)
