from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем маршруты приложения `shop`
    path('shop/', include('shop.urls')),
]