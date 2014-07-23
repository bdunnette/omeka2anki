omeka2anki
==========
Take an [Omeka](http://omeka.org) 2.1+ collection and output it as an [Anki](http://ankisrs.net)-compatible package.

Installation
------------
To use omeka2anki:

- Install [Python](https://www.python.org/downloads/) and [pip](http://pip.readthedocs.org/en/latest/installing.html#install-pip) (if they're not already on your system - Mac OS X and Linux should already have Python!)
- Download additional libraries that omeka2anki relies upon: `pip install -r requirements.txt`
- Copy o2a_settings.py.dist to o2a_settings.py
- Edit o2a_settings.py to reflect your Omeka setup:
  - Change `API_ENDPOINT` to your Omeka API location - e.g. `["http://archive.pathology.umn.edu/api/"]`; if you have more than one repository, use something like `["http://omeka-repository1/api/", "http://omeka-repository2/api/"]`
  - Change `OUTPUT_DIR` to be the path where generated decks will be placed, e.g. `/home/myusername/omeka2anki`
- Run omeka2anki: `python omeka2anki.py`
  
Anki packages (.apkg files) for each publicly-available Omeka collection should now be created in the specified folder.

Questions or issues? Please report them here: https://github.com/bdunnette/omeka2anki/issues
