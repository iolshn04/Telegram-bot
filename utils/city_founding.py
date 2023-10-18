import requests
import json
from config_data.config import RAPID_API_KEY


def city_found(city):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    cities = {}

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        for i_elem in data['sr']:
            if i_elem['type'] == "CITY" or i_elem['type'] == "NEIGHBORHOOD":
                cities[i_elem['gaiaId']] = i_elem['regionNames']['fullName']

        return cities
    else:
        raise LookupError('Запрос пуст...')
# with open('file.json', 'w', encoding='utf-8') as file:
#     json.dump(response.json(), file, indent=4, ensure_ascii=False)

# with open('file.json', 'r') as f:
#     file_content = f.read()
#     templates = json.loads(file_content)
#
# for i_elem in templates['sr']:
#     if i_elem['type'] == "CITY" or i_elem['type'] == "NEIGHBORHOOD":
#         print(i_elem['gaiaId'])
#         print(i_elem['regionNames']['fullName'])
