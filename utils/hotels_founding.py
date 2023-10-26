from loguru import logger
import requests
import json

from config_data.config import RAPID_API_KEY
from utils.hotel_detail import hotel_detail


def hotel_found(hotels, sort):
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
            "year": hotels['check_out_date']['year']
        },
        "rooms": [
            {
                "adults": hotels['adults'],
                "children": hotels['children']
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": sort
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    logger.debug(payload)
    logger.debug(url)
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

#
# with open('file2.json', 'w', encoding='utf-8') as file:
#     json.dump(response.json(), file, indent=4, ensure_ascii=False)

# #
# with open('file2.json', 'r') as f:
#     file_content = f.read()
#     templates = json.loads(file_content)
#
#     perk = 'black'
#     if perk == 'bla':
#         high = -1
#     else:
#         high = 1
#     count = 0
#     for i_elem in templates['data']['propertySearch']["properties"][:40]:
#         count += 1
#         # print(i_elem)
#         print(count)
#         # print(i_elem['offerSummary']['messages'][0]['message'])
#         # name_hotel = i_elem['name']
#         # print('Имя отеля', name_hotel)
#         # id_hotel = i_elem['id']
#         # print('Id отеля', id_hotel)
#         # # period = i_elem['price']['priceMessages'][1]['value']
#         # # print('Период', period)
#         # score = i_elem['reviews']['score']
#         # print('Id отеля', score)
#
#         # price = i_elem['price']['options'][0]['formattedDisplayPrice']
#         # print('Цена за ночь', price)
#         total_price = i_elem['price']['lead']['amount']
#
#         print('Цена за период', total_price)
#         # photo_hotel = hotel_detail(id_hotel, hotels['photo_count'])
