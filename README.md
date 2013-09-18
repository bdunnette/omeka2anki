omeka2anki
==========
Take an [Omeka](http://omeka.org) 2.1+ collection and output it as an [Anki](http://ankisrs.net)-compatible package.

Installation
------------
To use omeka2anki:

- Install [Python](http://python.org) (if it's not already on your system)
- Download additional libraries that omeka2anki relies upon:
  
	_pip install -r requirements.txt_
  
- Copy omeka_api_config.py.dist to omeka_api_config.py
- Edit omeka_api_config.py to reflect your Omeka setup (changing API_ENDPOINT to your Omeka API location - usually something like http://your-server-name-here/api)
- Run omeka2anki:
  
	_python omeka2anki.py_
  
Anki packages (.apkg files) for each publicly-available Omeka collection should be created in the _omeka2anki-temp_ folder in your home directory.
