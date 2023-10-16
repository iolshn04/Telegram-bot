import requests
import json

from config_data.config import RAPID_API_KEY


def hotel_found(hotels):
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": hotels['destination_id']},
        "checkInDate": {
            "day": hotels['check_in_date']['day'],
            "month": hotels['check_in_date']['month'],
            "year": hotels['check_in_date']['year']
        },
        "checkOutDate": {
            "day": hotels['check_out_date']['day'],
            "month": hotels['check_out_date']['month'],
            "year": hotels['check_out_date']['month']
        },
        "rooms": [
            {
                "adults": hotels['adults'],
                "children": hotels['children']
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 150,
            "min": 100
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())



# with open('file2.json', 'w', encoding='utf-8') as file:
#     json.dump(response.json(), file, indent=4, ensure_ascii=False)

# with open('file2.json', 'r') as f:
#     file_content = f.read()
#     templates = json.loads(file_content)
#
# for i_elem in templates['data']['propertySearch']["properties"]:
#     print(i_elem)
#     # if i_elem['type'] == "CITY" or i_elem['type'] == "NEIGHBORHOOD":
#     #     print(i_elem['gaiaId'])
#     #     print(i_elem['regionNames']['fullName'])