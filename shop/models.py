from django.db import models
import uuid


class Shop(models.Model):
    shop_id = models.IntegerField(unique=True)
    secret_key = models.CharField(max_length=255, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shop_id}"


class APIUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    api_key = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = self.generate_key()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return str(uuid.uuid4())
