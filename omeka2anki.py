# -*- coding: utf-8 -*-
# Copyright 2013-2014 Regents of the University of Minnesota
# Available under the terms of the MIT License: http://opensource.org/licenses/MIT

import requests
import json
import sys
from pprint import pprint
from urllib import urlretrieve
import os.path
import re
import string
import time
from dateutil.parser import *
from dateutil.tz import *
from datetime import *
import calendar
import hashlib

import o2a_settings

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
    repositories = o2a_settings.REPOSITORIES
    my_collections = []
    for repo in repositories:
	print repo
	
	now = str(calendar.timegm(datetime.utcnow().timetuple()))

	auth_hash = hashlib.sha1(now + repo['secret']).hexdigest()
	
 	headers = {
		"Authorization-User": repo['user'],
		"Authorization-Key": repo['key'],
		"Authorization-Timestamp": now,
		"Authorization-Hash": auth_hash		
	}
	print headers
	asset_id = "554a941b5d6fdfd3430bc782"
	r = requests.post(repo['url'] + "asset/assetLookup/" + asset_id, headers=headers)	
	print(r.url)
	print(r.text)

if __name__ == "__main__":
    main()
