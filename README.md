# ORBIT
## Optimized Retrieval for Beyond Interstellar Technologies

<figure>
    <img 
    src="./imgs/ORBIT_banner.png" 
    alt='HdM X Stuttgart University'
    >
</figure>

![status](https://img.shields.io/badge/status-in%20development-yellow)

---



docker exec -it solr-server solr create_core -c orbit

docker exec -it solr-server solr config -c orbit --action set-user-property --property update.autoCreateFields --value false

<str name="field">spellcheck_base</str>
<str name="spellcheck">true</str>

TODO:
- Ich habe im index dupmlikate wegen dem spellcheck --> Das Schema nochmal anschauen
- Faccetieren ist visuell da aber man kann damit nichts amchen.
- Doku/ReadMe schreiben
