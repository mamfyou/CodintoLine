from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class CodintoLineUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name='نام کاربری')
    password = models.CharField(max_length=60, verbose_name='رمز عبور')
    email = models.EmailField(verbose_name='ایمیل')
    phone_number = models.CharField(max_length=12, validators=[
        RegexValidator(regex='^09[0-9]{9}$', message='شماره تلفن همراه وارد شده صحیح نمی باشد')],
                                    verbose_name='تلفن همراه')
    REQUIRED_FIELDS = ["email", "phone_number"]


class Folder(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name
