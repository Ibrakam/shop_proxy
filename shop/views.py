import json
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .models import Shop, APIUser


@csrf_exempt
def send_data_to_octo(request):
    """
    Принимает POST-запрос (JSON), проверяет octo_shop_id, 
    проксирует запрос к Octo и возвращает ответ.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    api_key = request.META.get('HTTP_X_API_KEY', None)  # заголовок X-API-Key
    if not api_key:
        api_key = request.GET.get('api_key')

        # 3) Если по-прежнему нет, посмотрим в теле (если это JSON)
        #    (Поскольку метод POST, можно разобрать request.body)
    if not api_key:
        try:
            data = json.loads(request.body)
            api_key = data.get('api_key')
        except (json.JSONDecodeError, AttributeError):
            pass

        # 4) Если ключ так и не нашли — возвращаем 401
    if not api_key:
        return JsonResponse({'error': 'API key is missing'}, status=401)

        # 5) Проверяем, существует ли такой ключ в базе
    try:
        user_api_key = APIUser.objects.get(key=api_key)
    except APIUser.DoesNotExist:
        return JsonResponse({'error': 'Invalid API key'}, status=403)

    # Читаем входящий JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Проверяем, что есть ключ octo_shop_id
    if 'octo_shop_id' not in data:
        return JsonResponse({"error": "octo_shop_id is required"}, status=400)

    # Проверяем, что такой shop_id есть в базе
    shop_id_value = data['octo_shop_id']

    if not Shop.objects.filter(shop_id=shop_id_value).exists():
        return JsonResponse({"error": "Нет доступа (Shop ID не найден)"}, status=403)

    # Проксируем все поля, как есть
    octo_data = data

    # Берём URL к Octo из настроек (см. settings.py)
    octo_api_url = settings.OCTO_API_URL

    # Отправляем запрос к Octo
    try:
        response = requests.post(octo_api_url, json=octo_data, timeout=60)
        # Если код не 2xx, выбросим исключение
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)

    # Возвращаем JSON-ответ от Octo
    return JsonResponse(response.json(), safe=False, status=response.status_code)
