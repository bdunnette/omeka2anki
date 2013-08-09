import requests
import json
import sys
import pprint
import omeka_api_config
import anki, anki.exporting

api_endpoint = omeka_api_config.API_ENDPOINT
api_key = omeka_api_config.API_KEY
collection_id = "4"

omeka_collection = requests.get(api_endpoint + "collections/" + collection_id).json()
#pprint.pprint(omeka_collection)
anki_collection = anki.storage.Collection("test.anki2")
pprint.pprint(anki_collection.__dict__)
anki_note = anki_collection.newNote()
anki_note.fields = ["<img src='Humhrt2.jpg'>", "Human heart"]
anki_collection.addNote(anki_note)
pprint.pprint(anki_note.__dict__)
anki_collection.media.addFile("C:\\temp\\Humhrt2.jpg")
anki_collection.save()
anki_exporter = anki.exporting.AnkiPackageExporter(anki_collection)
anki_exporter.exportInto("C:\\temp\\test.apkg")
cards = requests.get(api_endpoint + "items?collection=" + collection_id).json()
#pprint.pprint(cards)