import requests
import json
import sys
import pprint
import omeka_api_config
import csv

api_endpoint = omeka_api_config.API_ENDPOINT
api_key = omeka_api_config.API_KEY

title_element = requests.get(api_endpoint + "elements?name=Title").json()
print title_element
title_element_id = title_element[0]['id']

image_descriptions = csv.reader(open('image_descriptions.csv', 'r'), delimiter="|")
images = {}

for image in image_descriptions:
    images[image[0] + ":" + image[1]] = image[2]
item_list = requests.get(api_endpoint + "items?per_page=250").json()
for item in item_list:
    case_title = item['element_texts'][0]['text'].strip()
    print case_title
    item_files = requests.get(api_endpoint + "files?item=" + str(item['id'])).json()
    for file in item_files:
        if not file['element_texts']:
            filename = file['original_filename'].rsplit("/",1)[1]
            file_key = ":".join([case_title, filename])
            if file_key in images:
                new_element = {'name': 'title', 'text': images[file_key], 'html': False, 'element': {'id': title_element_id}}
                print new_element
                file['element_texts'] = [new_element]
                file_update_url = '%sfiles/%s?key=%s' % (api_endpoint, file['id'], api_key)
                print file_update_url
                file_updated = requests.put(file_update_url, data=json.dumps(file))