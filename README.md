# ORBIT  
## Optimized Retrieval for Beyond Interstellar Technologies

<figure>
  <img src="./imgs/ORBIT_banner.png" alt="HdM X Stuttgart University" />
</figure>

![Status](https://img.shields.io/badge/status-in%20development-yellow)

---

## Projektübersicht

ORBIT ist ein Such- und Retrieval-System, das auf Apache Solr basiert und für Beyond Interstellar Technologies optimiert wurde.  
Ziel ist die effiziente und präzise Suche in großen Datenbeständen, unterstützt durch intelligente Features wie Spellchecking und Facettierung.

---

## Aktueller Stand

- Entwicklung aktiv
- Core „orbit“ wurde erfolgreich in Solr angelegt und konfiguriert
- Grundlegendes Spellchecking aktiviert
- Facettierung bereits visualisiert, aber noch nicht interaktiv nutzbar
- Dokumentation und README in Arbeit

---

## Installation & Setup

### Solr Core anlegen

```bash
docker exec -it solr-server solr create_core -c orbit
```

###Core-Konfiguration anpassen```bash
```bash
docker exec -it solr-server solr config -c orbit --action set-user-property --property update.autoCreateFields --value false
```

### Wichtige Schema-Einstellungen (Beispiel)
```xml
<str name="field">spellcheck_base</str>
<str name="spellcheck">true</str>
```

## Hinweise & Kontakt
Für Fragen, Feedback oder Mitwirkung am Projekt kontaktiere bitte das Team bei Beyond Interstellar Technologies oder die Entwickler an den beteiligten Hochschulen (HdM Stuttgart & Universität Stuttgart).

---

Vielen Dank für dein Interesse an ORBIT!