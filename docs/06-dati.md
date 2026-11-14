# 06 — Strategia dati

Stato: **piano iniziale**. Ogni fonte va verificata (licenza, termini, qualità) dal `data-engineer` prima dell'uso.

## Principio
Il modello nasce da tre fonti, in quest'ordine di importanza:
1. **Eventi reali degli utenti** (partenze e segnalazioni anonime). È la fonte più importante, ma arriva solo dopo il lancio della beta.
2. **Dati aperti e infrastruttura** (strade, sosta regolamentata, zone, tariffe, POI).
3. **Priori storici e modelli di domanda** (ora, giorno, uffici, scuole, stazioni, eventi).

Nell'iterazione 0–1 non esistono dati reali di occupazione. Questo va dichiarato in ogni report: **ogni stima prima della beta è un prior, non una misura.**

## Fonti

| Fonte | Cosa fornisce | Licenza / termini | Stato |
|---|---|---|---|
| **Comune di Milano — Open Data** (dati.comune.milano.it) | Tariffe per ambito di sosta; GTFS ATM; sosta bici e bus turistici | CC BY 4.0 sui dataset visti (verificare per ogni dataset al download) | Parziale. Stalli/sensori strisce blu: vedi esito sotto |
| **ATM / Sosta Milano** (gestore della sosta per il Comune) | Zone, tariffe, orari strisce blu | Da verificare | Da contattare solo su decisione del fondatore |
| **OpenStreetMap** | Rete stradale, parcheggi, POI | ODbL (attribuzione obbligatoria, share-alike sui dati derivati) | Utilizzabile, da documentare |
| **ISTAT** (basi territoriali, sezioni di censimento 2021) | Confini sezioni, popolazione, densità | CC BY 4.0 (da documenti ISTAT) | Utilizzabile (shapefile/CSV) |
| **Open-Meteo** | Meteo storico e previsioni | Dati CC BY 4.0; API gratuita solo uso non commerciale (<10.000 chiamate/giorno) | Prototipo ok. Uso commerciale richiede piano a pagamento: decisione del fondatore |
| **Google Routes / Maps Platform** | Percorsi, navigazione, visualizzazione | Termini restrittivi su caching e bulk | Solo percorsi e visualizzazione (D-004) |
| **Eventi della città** (portale Comune o fonti pubbliche) | Eventi che cambiano la domanda di sosta | Da verificare | Da valutare |
| **Dati degli utenti** | Eventi anonimi di partenza e segnalazioni | Consenso dell'utente (vedi `03-privacy.md`) | Dalla iterazione 2 |

## Esito verifica T-001 (consultazione 2026-11-14)

Limite del metodo: dal sandbox `dati.comune.milano.it`, `open-meteo.com` e gli altri host non erano raggiungibili (DNS). L'esito deriva da ricerche web e snippet, non da navigazione del catalogo. Va riconfermato appena l'host è consentito.

**Stalli o sensori strisce blu: NON TROVATI.** Nessun dataset di stalli georeferenziati, occupazione o sensori per la sosta su strada. Esito: non esiste (o non è pubblicato), con confidenza media per il limite sopra. Nessun risultato web riporta sensori sulle strisce blu.

| Tema | Esito | Dettagli |
|---|---|---|
| Tariffe per ambito di sosta | Esiste | Campi: ambito, costo_g, costo_s, res_giorno, res_sera, tipo_sosta, delibera. CC BY 4.0. Agg. 2025-04-03 |
| Stalli su strada / sensori | Non esiste | Solo cifre di stampa e presentazioni: circa 83.000 stalli blu (stampa), circa 39.000 stalli pubblici (presentazione Comune 2024). Incoerenti: non usare come input |
| Sosta bici (ds670), bus turistici (ds740) | Esiste, non rilevante | CSV, CC BY 4.0. Non per auto |
| GTFS ATM (ds929, `dati.comune.milano.it/gtfs.zip`) | Esiste | Metro, tram, bus. Validità osservata 2026-05-04 / 2026-06-12: probabilmente scaduta, riscaricare |
| Area C / Area B, lavaggio strade, mercati rionali, parcheggi di struttura e interscambio | Non confermato | Non emersi dalle ricerche. Zone Area B/C ricavabili da fonti ufficiali del Comune/AMAT. Resta da cercare nel catalogo |
| AMAT Report della Mobilità | Solo PDF | Aggregati su Area C/B e sosta. Licenza non verificata |

**Open-Meteo:** termini ufficiali: API gratuita solo non commerciale, dati CC BY 4.0 con attribuzione. Per il rilascio commerciale serve piano a pagamento (D-004 analogo: decisione umana).

**OSM:** tag utili: `amenity=parking`, `parking=street_side|lane|surface|multi-storey`, `parking:lane:*` (`parking:left/right/both`, `:orientation`, `:fee`, `:capacity`), `access`, `fee`, `maxstay`, `capacity`, `amenity=parking_space`. Copertura a Milano: non misurata. Da quantificare via Overpass in un task (non in bulk dal servizio pubblico: usare estratto Geofabrik).

## Stime di partenza da verificare
- Il numero di stalli su strada a Milano non ha fonte ufficiale coerente (vedi tabella). Non usarlo come input.
- Il numero di sanzioni per sosta irregolare (2026) è riportato dalla stampa. Da verificare prima di citarlo in materiale pubblico.
- Area C nel weekend a pagamento dal 2026-01-01: riportato da siti secondari, da confermare su fonte ufficiale.

## Conseguenza per il modello
Senza stalli né sensori, la capacità per segmento va stimata da OSM (`parking:lane:*`) e dalla tariffa per ambito. Resta un prior, non una misura (vedi Principio).

## Strategia di raccolta

1. **Iterazione 1:** costruzione della base (rete, parcheggi, zone, POI) da fonti aperte.
2. **Iterazione 1:** test sintetici per verificare la pipeline. I risultati sono dichiarati come test, non come accuratezza.
3. **Iterazione 2:** raccolta eventi reali con beta tester. Obiettivo minimo: 500 eventi in centro.
4. **Iterazione 3:** calibrazione continua. Ogni cella ha un contatore di eventi e un indicatore di affidabilità.

## Regole
- Nessun dato personale grezzo nel repository. Gli esempi usano dati sintetici chiaramente etichettati.
- Ogni dataset ha un file di metadati: fonte, data di download, licenza, versione.
- Nessun dato di Google salvato in blocco.
- I dati sintetici non entrano mai nelle metriche di produzione.
