# -*- coding: utf-8 -*-
# Copyright 2103 Regents of the University of Minnesota
# Available under the terms of the MIT License: http://opensource.org/licenses/MIT

import requests
import json
import sys
import pprint
from urllib import urlretrieve
import os.path

import omeka_api_config

import anki, anki.exporting

api_endpoint = omeka_api_config.API_ENDPOINT

root_path = os.path.join(os.path.expanduser('~'), 'omeka2anki-temp')
omeka_collections = requests.get(api_endpoint + "collections").json()
for omeka_collection in omeka_collections[1:]:
    collection_name = omeka_collection['element_texts'][0]['text'].lower().replace(' ','_')
    omeka_items = requests.get(omeka_collection['items']['url']).json()
    print "Found collection %s with %s items" % (collection_name, len(omeka_items))#pprint.pprint(omeka_collection)
    if len(omeka_items) >= 1:
        anki_collection = anki.storage.Collection(os.path.join(root_path, "%s.anki2" % collection_name))
        for item in omeka_items:
            item_files = requests.get(item['files']['url']).json()
            item_file_dict = {f['original_filename']:f for f in item_files}
            for item_file in item_files:
                #print file
                if ('image' in item_file['mime_type']) and ('_marked' not in item_file['original_filename']):
                    anki_note = anki_collection.newNote()
                    card_back = ""
                    print "Downloading file %s" % item_file['filename']
                    file_image = urlretrieve(item_file['file_urls']['original'], os.path.join(root_path, item_file['filename']))
                    anki_collection.media.addFile(os.path.join(root_path, item_file['filename']))
                    base_filename = item_file['original_filename'].rsplit("/",1)[1]
                    marked_filename = base_filename.replace(".jpg", "_marked.jpg")
                    if marked_filename in item_file_dict:
                        marked_file = item_file_dict[marked_filename]
                        print "Downloading marked file %s" % marked_file['filename']
                        file_image = urlretrieve(marked_file['file_urls']['original'], os.path.join(root_path, marked_file['filename']))
                        anki_collection.media.addFile(os.path.join(root_path, marked_file['filename']))
                        card_back += "<img src='%s'>" % marked_file['filename']
                    elif item_file['element_texts']:
                        card_back += item_file['element_texts'][0]['text']
                    else:
                        break
                    anki_note.fields = ["<img src='%s'>" % item_file['filename'], card_back]
                    anki_collection.addNote(anki_note)
                    # pprint.pprint(anki_note.__dict__)
        
        print "Saving collection %s" % collection_name 
        anki_collection.save()
        anki_exporter = anki.exporting.AnkiPackageExporter(anki_collection)
        print "Exporting to %s.apkg" % collection_name
        anki_exporter.exportInto(os.path.join(root_path, "%s.apkg" % collection_name))
