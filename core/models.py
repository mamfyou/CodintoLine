from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tokens')

    def __str__(self):
        return self.token