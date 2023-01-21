from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class CodintoLineUser(AbstractUser):
    password = models.CharField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=12, validators=[
        RegexValidator(regex='^09[0-9]{9}$', message='شماره تلفن همراه وارد شده صحیح نمی باشد')],
                                    verbose_name='تلفن همراه', unique=True)
    USERNAME_FIELD = "phone_number"


class Folder(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='folderOwner')

    def __str__(self):
        return self.name
