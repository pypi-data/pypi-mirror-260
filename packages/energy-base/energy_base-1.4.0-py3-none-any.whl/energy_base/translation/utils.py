import os

import requests
from django.utils.translation import get_language


def translate(key: str) -> str:
    base_url = os.environ.get('TRANSLATION_SERVICE_URL')
    return requests.get(f'{base_url}/translations/{key}', headers={
        'Accept-Language': get_language()
    }).text
