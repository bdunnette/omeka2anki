# -*- coding: utf-8 -*-
# Copyright 2103 Regents of the University of Minnesota
# Available under the terms of the MIT License: http://opensource.org/licenses/MIT

import requests
import json
import sys
import pprint
from urllib import urlretrieve
import os.path
import re
import string  

import settings

import anki, anki.exporting

# From http://www.andrew-seaford.co.uk/generate-safe-filenames-using-python/
## Make a file name that only contains safe charaters  
# @param inputFilename A filename containing illegal characters  
# @return A filename containing only safe characters  
def makeSafeFilename(inputFilename):     
    try:  
        safechars = string.letters + string.digits + " -_."  
        return filter(lambda c: c in safechars, inputFilename).replace(" ","_")
    except:  
	   return ""    
    pass  

def main():
    omeka_repositories = settings.REPOSITORIES
    for api_endpoint in omeka_repositories:
        settings.OUTPUT_DIR = os.path.join(os.path.expanduser('~'), 'omeka2anki-temp')
        title_element = requests.get(api_endpoint + "elements?name=Title&element_set=1").json()
        title_element_id = title_element[0]['id']
        omeka_collections = requests.get(api_endpoint + "collections").json()
        for omeka_collection in omeka_collections[1:]:
            collection_name = omeka_collection['element_texts'][0]['text']
            collection_filename = makeSafeFilename(collection_name).lower()
            collection_tag = re.sub('[^0-9a-zA-Z]+', '', collection_name.split(":")[0].lower().strip())
            omeka_items = requests.get(omeka_collection['items']['url']).json()
            print "Found collection %s with %s items" % (collection_name, len(omeka_items))
            if len(omeka_items) >= 1:
                # Create a new deck, which Anki calls a Collection
                print settings.OUTPUT_DIR
                anki_collection = anki.storage.Collection(os.path.join(settings.OUTPUT_DIR, "%s.anki2" % collection_filename))
                for item in omeka_items:
                    # Get the text of the item's 'Title' element
                    item_title = [element['text'] for element in item['element_texts'] if element['element']['id'] == title_element_id][0]
                    print item_title
                    item_files = requests.get(item['files']['url']).json()
                    item_file_dict = {f['original_filename']:f for f in item_files}
                    for item_file in item_files:
                        # Check to see if item is an image, and is not the annotated version of some other file
                        if ('image' in item_file['mime_type']) and ('_marked' not in item_file['original_filename']):
                            # Create a new card - a "note" in Anki terms
                            anki_note = anki_collection.newNote()
                            card_back = "<h3>%s</h3>" % item_title
                            anki_note.tags = [collection_tag]
                            
                            # If image hasn't been downloaded, fetch it
                            image_filename = os.path.join(settings.OUTPUT_DIR, item_file['filename'])
                            if not os.path.isfile(image_filename):
                                print "Downloading file %s" % item_file['filename']
                                file_image = urlretrieve(item_file['file_urls']['original'], image_filename)
                                
                            # Add image to the media in this card deck
                            anki_collection.media.addFile(image_filename)
                            
                            # Look to see if there is a "_marked" version of this image
                            if "/" in item_file['original_filename']:
                                base_filename = item_file['original_filename'].rsplit("/",1)[1]
                            else:
                                base_filename = item_file['original_filename']
                            marked_filename = base_filename.replace(".jpg", "_marked.jpg")
                            
                            # If so, download the _marked file and add to the collection
                            if marked_filename in item_file_dict:
                                marked_file = item_file_dict[marked_filename]
                                marked_filename_local = os.path.join(settings.OUTPUT_DIR, marked_file['filename'])
                                if not os.path.isfile(marked_filename_local):
                                    print "Downloading marked file %s" % marked_file['filename']
                                    file_image = urlretrieve(marked_file['file_urls']['original'], marked_filename_local)
                                anki_collection.media.addFile(marked_filename_local)
                                card_back += "<img src='%s'>" % marked_file['filename']
                            # If item has descriptive text, add it to the back of the card
                            if item_file['element_texts']:
                                card_back += "<p>%s</p>" % item_file['element_texts'][0]['text']
                            
                            print "Card Back: " + card_back
                            anki_note.fields = ["<img src='%s'>" % item_file['filename'], card_back]
                            anki_collection.addNote(anki_note)
                            
                print "Saving collection %s" % collection_name 
                anki_collection.save()
                anki_exporter = anki.exporting.AnkiPackageExporter(anki_collection)
                print "Exporting to %s.apkg" % collection_filename
                anki_exporter.exportInto(os.path.join(settings.OUTPUT_DIR, "%s.apkg" % collection_filename))

if __name__ == "__main__":
    main()