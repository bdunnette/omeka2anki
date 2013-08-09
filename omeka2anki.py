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
    collection_name = omeka_collection['element_texts'][0]['text'].lower()
    print "Found collection %s with %s items" % (collection_name, len(omeka_collection['items']))
    #pprint.pprint(omeka_collection)
    anki_collection = anki.storage.Collection("%s.anki2" % collection_name)
    omeka_items = requests.get(omeka_collection['items']['url']).json()
    for item in omeka_items:
        #print item
        item_files = requests.get(item['files']['url']).json()
        #print item_files
        for file in item_files:
            if file['element_texts']:
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
