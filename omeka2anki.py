# -*- coding: utf-8 -*-
# Copyright 2103 Regents of the University of Minnesota
# Available under the terms of the MIT License: http://opensource.org/licenses/MIT

import requests
import json
import sys
import pprint
from urllib import urlretrieve
import omeka_api_config
import anki, anki.exporting

api_endpoint = omeka_api_config.API_ENDPOINT

omeka_collections = requests.get(api_endpoint + "collections").json()
for omeka_collection in omeka_collections:
    collection_name = omeka_collection['element_texts'][0]['text'].lower().replace(' ','_')
    omeka_items = requests.get(omeka_collection['items']['url']).json()
    print "Found collection %s with %s items" % (collection_name, len(omeka_items))#pprint.pprint(omeka_collection)
    if len(omeka_items) >= 1:
        anki_collection = anki.storage.Collection("%s.anki2" % collection_name)
        for item in omeka_items:
            #print item
            item_files = requests.get(item['files']['url']).json()
            #print item_files
            for file in item_files:
                print file
                if file['element_texts'] and 'image' in file['mime_type']:
                    anki_note = anki_collection.newNote()
                    print "Downloading file %s" % file['filename']
                    file_image = urlretrieve(file['file_urls']['thumbnail'], file['filename'])
                    card_back = file['element_texts'][0]['text']
                    anki_note.fields = ["<img src='%s'>" % file['filename'], card_back]
                    anki_collection.addNote(anki_note)
                    # pprint.pprint(anki_note.__dict__)
                    anki_collection.media.addFile(file['filename'])

        print "Saving collection %s" % collection_name 
        anki_collection.save()
        anki_exporter = anki.exporting.AnkiPackageExporter(anki_collection)
        print "Exporting to %s.apkg" % collection_name
        anki_exporter.exportInto("C:\\temp\\%s.apkg" % collection_name)
