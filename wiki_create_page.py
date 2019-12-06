#!/usr/bin/env python3

paste_text = """
# Treffen DATUM_PLACEHOLDER

**Termin:** 19:00 Uhr, DATUM_PLACEHOLDER, Start und Neulingsbegrüßung, 19:30 Uhr Eröffnung der Tagesordnung

**Ort:** Hackerspace Bremen e.V. ([Anfahrt](https://www.hackerspace-bremen.de/anfahrt/))

## Tagesordnung
### Neulingsbegrüßung (19:00 – 19:30 Uhr)

- Abfragen:
    - ist jemand neu?
    - hat jemand Fragen?
    - braucht jemand Hilfe?
- Einführung:
    - kurze Vorstellungsrunde
    - Funktionsweise der Freifunk Community
    - wie verschieden können die Beiträge/Funktionen eines Freifunker sein (TOP Aufgaben)
    - Ablauf des Treffens

---

### Top 1: Termine übertragen
- Ins letzte Protokoll gucken und Termine übertragen

### Top 2
...


### Termine
...

## Regelmäßige TOPs
### Aufgaben

- hat jemand Kapazität / möchte jemand helfen?
- ein paar Aufgaben von https://tasks.ffhb.de/ anbieten

### Rechte

- Zustand
- Zufriedenheit
- Änderungen?

### Treffen abschließen

- Info zu Treffen aktualisieren
  - Protokoll aus Pad ins Wiki kopieren
  - neue Wiki-Seite für nächstes Treffen mit Standard-TOPs anlegen
  - [Treffen auf Wiki-Homepage anpassen](https://wiki.bremen.freifunk.net/Home)
  - Topic im IRC anpassen
- Aufräumen!
  - Müll weg
  - Kabel zurück

## Protokoll

Live Kollaboration:

* Schreiblink: https://hackmd.io/AwDgnA7ATArKC0BGGBjAzPALAUzSeARgYgGzxQAmEFFwiKBEKAhkA===?edit
* Side-by-side: https://hackmd.io/AwDgnA7ATArKC0BGGBjAzPALAUzSeARgYgGzxQAmEFFwiKBEKAhkA===?both
* Leselink: https://hackmd.io/AwDgnA7ATArKC0BGGBjAzPALAUzSeARgYgGzxQAmEFFwiKBEKAhkA===?view

# Freifunk Bremen - Protokoll-Pad

### Anwesende
"""

import requests as req
import time
import logging

LOG_FILENAME = 'log_wiki_create.log'
FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(filename=LOG_FILENAME,format=FORMAT,level=logging.INFO)

host = 'https://wiki.bremen.freifunk.net'
path = "/Treffen"
page = time.strftime("%Y_%m_%d") # Datum

user = 'XXX'
passwd = 'XXX'

###
### Friday check
###

def main():
	if int(time.strftime("%w")) == 5:
		# its friyday
		logging.info("It's Friday!")
		if (int(time.strftime("%d")) <=  7) or (int((time.strftime("%d")) >= 15) and (int(time.strftime("%d")) < 22)):
			# first or third friday!
			logging.info("And 1st or 3rd! Wow!")
			check_existing()
		else:
			logging.info("But not 1st or 3rd Friday.")
	else:
		logging.info("No Friday today :(")

	#logging.info("Don't care. Let's create!")
	#check_existing()

###
### Checks if page existing
###

def check_existing():
	global user
	global passwd
	global host
	global page
	
	url = host+"/create"+path+"/"+page

  # login
	resp_check = req.get(url, auth=(user, passwd))
	
  # get title
	title = resp_check.text
	title = title[title.find('<title>') + 7 : title.find('</title>')]
	
  # compare title
	if title == "Create a new page":
		logging.info("Page not existing. Creating...")
		create_page(page)
	else:
		logging.info("Page is existing. Will not be created again.")

###
### Create Page
###

def create_page(correct_title = "DATUM"):

	global user
	global passwd
	global host
	global path
	global paste_text

	demo_title = "justcreatedpagewithawrongnamekzb"
  
	create_post_req = {"page":demo_title,
			 "path": path,
			 "format":"markdown",
			 "content":paste_text.replace("DATUM_PLACEHOLDER", time.strftime("%d.%m.%Y")),
			 "message":"Created+"+demo_title}

	resp_create = req.post(host+"/create", data = create_post_req, auth=(user, passwd))
	
	###
	### Raname Page
	###
	
	rename_post_req = {"rename":path+"/"+correct_title,
			  		   "message":"Renamed+"+demo_title+"+to+"+correct_title}
			   
	resp_rename = req.post(host+"/rename"+path+"/"+demo_title, data = rename_post_req, auth=(user, passwd))

	logging.info("finish")
		   
main()
