# ORBIT
## Optimized Retrieval for Beyond Interstellar Technologies

![status](https://img.shields.io/badge/status-in%20development-yellow)

---

sudo systemctl stop flaskapp.service

sudo systemctl disable flaskapp.service

sudo systemctl start flaskapp.service

sudo systemctl enable flaskapp.service



docker exec -it solr-server solr create_core -c orbit

docker exec -it solr-server solr config -c orbit --action set-user-property --property update.autoCreateFields --value false

<str name="field">spellcheck_base</str>
<str name="spellcheck">true</str>

TODO:
- Ich habe im index dupmlikate wegen dem spellcheck --> Das Schema nochmal anschauen
- Faccetieren ist visuell da aber man kann damit nichts amchen.
- Doku/ReadMe schreiben