import requests
import json

from config_data.config import RAPID_API_KEY


def hotel_detail(id, count):
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    photo = []
    response = requests.post(url, json=payload, headers=headers)
    templates = response.json()
    for i_elem in templates['data']['propertyInfo']['propertyGallery']['images'][:count]:
        photo.append(i_elem['image']['url'])

    return photo

# with open('file3.json', 'r') as f:
#     file_content = f.read()
#     templates = json.loads(file_content)
#
# for i_elem in templates['data']['propertyInfo']['propertyGallery']['images'][:7]:
#     print(i_elem['image']['url'])
