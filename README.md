# ffhb-top-page-creator
Creates a wiki page with an agenda template if the page does not already exist.

# Cronjob
Use e.g. 
<code>
crontab -e
</code>

with

<code>
30 7 * * * python3 /home/wiki_create_page.py
</code>
