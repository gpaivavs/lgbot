import requests
import json

def get_card(cardname=''):
    cardname = cardname.replace(' ','+')
    url = f'https://api.scryfall.com/cards/named?fuzzy={cardname}'
    response = requests.get(url)
    response_json = response.json()
    imagens = response_json['image_uris']
    large = imagens['large']

    prices = response_json["prices"]
    usd = prices["usd"]
    return large,usd

