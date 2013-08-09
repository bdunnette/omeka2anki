import requests
import json
import sys
import pprint
import omeka_api_config

api_endpoint = omeka_api_config.API_ENDPOINT
api_key = omeka_api_config.API_KEY
collection_id = "4"

collection = requests.get(api_endpoint + "collections/" + collection_id).json()
pprint.pprint(collection)
cards = requests.get(api_endpoint + "items?collection=" + collection_id).json()
#pprint.pprint(cards)