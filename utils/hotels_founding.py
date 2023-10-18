import requests

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
        "sort": "PRICE_LOW_TO_HIGH"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response

    # for i_elem in template['data']['propertySearch']["properties"][:hotels['hotel_count']]:
    #     name_hotel = i_elem['name']
    #     print('Имя отеля', name_hotel)
    #     id_hotel = i_elem['id']
    #     print('Id отеля', id_hotel)
    #     period = i_elem['price']['priceMessages'][1]['value']
    #     print('Период', period)
    #     score = i_elem['reviews']['score']
    #     print('Id отеля', score)
    #     price = i_elem['price']['options'][0]['formattedDisplayPrice']
    #     print('Цена за ночь', price)
    #     total_price = i_elem['price']['displayMessages'][1]['lineItems'][0]['value']
    #     print('Цена за период', total_price)
    #     photo_hotel = hotel_detail(id_hotel, hotels['photo_count'])


# with open('file2.json', 'w', encoding='utf-8') as file:
#     json.dump(response.json(), file, indent=4, ensure_ascii=False)

# with open('file2.json', 'r') as f:
#     file_content = f.read()
#     templates = json.loads(file_content)

    # if i_elem['type'] == "CITY" or i_elem['type'] == "NEIGHBORHOOD":
    #     print(i_elem['gaiaId'])
    #     print(i_elem['regionNames']['fullName'])