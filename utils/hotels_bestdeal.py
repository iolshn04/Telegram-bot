from loguru import logger
import requests
import json

from config_data.config import RAPID_API_KEY
from utils.hotel_detail import hotel_detail


def hotel_bestdeal(hotels):
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
        "sort": "DISTANCE",
        "filters": {
            "price": {
                "max": hotels['max_price'],
                "min": hotels['min_price']
            }
        }
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
