# Diocèses français, belges et néerlandais (1592–1789) – Données géoréférencées

## 📖 Description

Ce dépôt propose un ensemble de fichiers **GeoJSON** représentant les diocèses catholiques en latin pour la période **1592–1789**, rattachés à leurs provinces ecclésiastiques selon les informations de la *Hierarchia Catholica*.

👉 Le fichier principal à consulter est : `carte_lat.geojson`.

Le projet est encore en cours de développement et sera progressivement enrichi.

Les données ont été **géoréférencées** afin de permettre leur exploitation dans des environnements de type **SIG**, des visualisations web ou des analyses en **humanités numériques**.

> ⚠️ Le géoréférencement repose sur des reconstitutions historiques et peut comporter des imprécisions.

---

## 🗂 Sources des données

- **Diocèses français :** article Wikipédia *Liste des diocèses de France sous l'Ancien Régime* (contributions, notamment, de Maxence Jeanjean)  
- **Diocèses belges et néerlandais :** André Tihon, *Clergé séculier et régulier des Pays-Bas autrichiens* (1786)  
- **Autres diocèses européens :** projet *EarthWorks* (Stanford University), complété par un travail personnel à partir de sources cartographiques historiques  

---

## 🌍 Géoréférencement

Le géoréférencement repose sur la localisation des **sièges épiscopaux historiques**.

Les données permettent :

- la visualisation cartographique des diocèses et des provinces ecclésiastiques  
- une analyse diachronique des évolutions diocésaines  

Pour la France, les variations sont prises en compte année par année (modifications territoriales, créations, suppressions).  
Pour les autres espaces, les évolutions reflètent principalement les changements de rattachement provincial.

---

## 📁 Format des données

Les fichiers sont fournis au format **GeoJSON** (`.geojson`).

Chaque entité comporte des propriétés standardisées. Exemple :

```json
"properties": {
  "diocese": "Aurasicen",
  "province": "Arelaten",
  "start": 1592,
  "end": 1789
}
```

- `diocese` : nom latin du diocèse  
- `province` : province ecclésiastique de rattachement  
- `start` / `end` : bornes chronologiques de validité (modifiées en cas d’évolution)

---

## ⚖️ Licence et attribution

Les données s’appuient sur :

- Wikipédia (licence **CC BY-SA**)  
- les travaux d’André Tihon  
- le projet *EarthWorks* (Stanford University)  

L’ensemble est donc diffusé sous licence **Creative Commons Attribution – Partage dans les Mêmes Conditions (CC BY-SA)**.

Merci de citer les sources originales ainsi que ce dépôt en cas de réutilisation.