from django.db.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
