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
            for file in item_files:
                #print file
                # Only create a card if we have both an image and descriptive text
                if 'image' in file['mime_type'] and file['element_texts']:
                    anki_note = anki_collection.newNote()
                    print "Downloading file %s" % file['filename']
                    file_image = urlretrieve(file['file_urls']['original'], os.path.join(root_path, file['filename']))
                    card_back = file['element_texts'][0]['text']
                    anki_note.fields = ["<img src='%s'>" % file['filename'], card_back]
                    anki_collection.addNote(anki_note)
                    # pprint.pprint(anki_note.__dict__)
                    anki_collection.media.addFile(os.path.join(root_path, file['filename']))

        print "Saving collection %s" % collection_name 
        anki_collection.save()
        anki_exporter = anki.exporting.AnkiPackageExporter(anki_collection)
        print "Exporting to %s.apkg" % collection_name
<<<<<<< HEAD
        anki_exporter.exportInto("C:\\Users\\dunn0172\\Google Drive\\%s.apkg" % collection_name)
=======
        anki_exporter.exportInto(os.path.join(root_path, "%s.apkg" % collection_name))
>>>>>>> 0d3bff15efe571b00cf436ae60fe6288850b2a01
