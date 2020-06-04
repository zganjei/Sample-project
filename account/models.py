from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    not_used = models.CharField("nothing", max_length=10, null=True, blank=True)
