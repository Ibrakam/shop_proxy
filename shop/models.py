from datetime import datetime, timedelta
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
    email = models.EmailField(blank=True, null=True)  # опциональное поле
    api_key = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Поля подписки
    subscription_start = models.DateTimeField(auto_now_add=True)  # старт подписки
    subscription_end = models.DateTimeField()  # дата окончания подписки

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Если API-ключ ещё не сгенерирован — создаём новый
        if not self.api_key:
            self.api_key = self.generate_key()

        # Если дата окончания подписки не задана — устанавливаем её на месяц вперёд
        if not self.subscription_end:
            self.subscription_end = self.subscription_start + timedelta(days=30)  # 1 месяц подписки

        super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return str(uuid.uuid4())

    def is_subscription_active(self) -> bool:
        """Проверяем, активна ли подписка."""
        return self.subscription_end >= datetime.now()

    def extend_subscription(self, days=30):
        """
        Продление подписки на указанное количество дней.
        По умолчанию продлеваем на 30 дней.
        """
        if self.subscription_end < datetime.now():
            # Если подписка истекла, начинаем новую с текущего дня
            self.subscription_start = datetime.now()
            self.subscription_end = self.subscription_start + timedelta(days=days)
        else:
            # Если подписка ещё активна, просто продлеваем её
            self.subscription_end += timedelta(days=days)
        self.save()
