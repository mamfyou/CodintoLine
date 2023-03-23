from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=255, verbose_name='توکن')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='tokens', verbose_name='کاربر')

    def __str__(self):
        return self.token
