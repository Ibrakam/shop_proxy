from django.db import models

# Create your models here.
from django.db import models


class Shop(models.Model):
    shop_id = models.CharField(max_length=255, unique=True)
    secret_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_id
