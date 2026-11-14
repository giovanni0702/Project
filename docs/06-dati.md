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

Metodo (ripresa 2026-11-14): interrogata l'API CKAN di `dati.comune.milano.it` (2617 dataset nel catalogo), letta direttamente. Home del Comune: 403; `open-meteo.com`, `atm.it`, `bikemi.com`, `geoportale`, `amat-mi.it`: bloccati dal proxy da questa sessione (esiti web = secondari).

**Stalli o sensori strisce blu: NON TROVATI.** Ricerche CKAN "sosta", "stalli", "strisce blu", "sensori", "parcheggi": nessun dataset di stalli georeferenziati, occupazione o sensori su strada. Esito: non esiste nel catalogo (confidenza alta). Un articolo del 2022 annunciava smart parking ATM con sensori: nessuna conferma che sia operativo.

| Tema | Esito | Dettagli |
|---|---|---|
| Ambiti della sosta (ds83) | Esiste (geometrie) | Poligoni degli ambiti: solo `ambito`, `nome`, `geom`. GeoJSON/SHP/CSV, CC BY 4.0, risorse agg. 2025-04-03 |
| Tariffe per ambito di sosta | **Non trovate nel catalogo** | Le 5 ricerche CKAN (tariffe, costo, res_giorno, tipo_sosta, ambiti) non restituiscono un dataset di tariffe. I campi `costo_g`, `res_giorno` citati prima non sono verificati: probabile confusione. Tariffe da pagina ufficiale Comune/ATM (403 da qui) |
| Stalli su strada / sensori | Non esiste | Solo cifre di stampa e presentazioni: circa 83.000 stalli blu (stampa), circa 39.000 stalli pubblici (presentazione Comune 2024). Incoerenti: non usare come input |
| Sosta bici (ds670), bus turistici (ds740) | Esiste, non rilevante | CSV, CC BY 4.0. Non per auto |
| GTFS ATM (ds929, `dati.comune.milano.it/gtfs.zip`) | Esiste, statico | Letto 2026-11-14: 25 MB, feed AMAT versione 425, inizio 2026-10-26, fine servizio 2026-11-30 (scade presto, serve riscarico periodico). Solo orari teorici |
| Varchi Area C (ds82) | Esiste | Posizione varchi, CC BY 4.0, agg. 2026-11-04 (campi id, label, geom) |
| Accessi Area C (ds779-ds818, ds862 e successivi, fino a "mensili novembre 2024") | Esiste, storico | Conteggi giornalieri/orari/mensili per varco, ~110 dataset, ultimo osservato nov. 2024. Decodifica campi: ds861. Non è tempo reale |
| Area B | Parziale | Nessun dataset dedicato. Solo ds51 "Aree pedonali e ZTL". Perimetro Area B da fonte ufficiale o OSM |
| Lavaggio strade / pulizia strade | **Non esiste** nel catalogo | Ricerche "lavaggio strade", "pulizia strade", "spazzamento", "pulizia" senza dataset utili (solo rifiuti urbani annuali) |
| Mercati | Esiste | ds291 (mercati settimanali scoperti), ds2471 (coperti), ds2629 (agricoltori). Verificare campi e giorni/orari al download |
| Parcheggi pubblici (ds342) e di interscambio (ds45) | Esiste, statico | GeoJSON/CSV/SHP, CC BY 4.0, creati da AMAT. Risorse del 2017-2020: dati vecchi, solo posizione/capacità, nessuna disponibilità live |
| Sharing (ds574, ds79, ds65) | Esiste, statico | ds574: serie annuale veicoli/prelievi 2011-2025. ds79 aree car sharing, ds65 stazioni BikeMi |
| Colonnine di ricarica (ds540) | Esiste | Posizione. Stalli riservati a EV: sottrae capacità alla sosta |
| AMAT Report della Mobilità | Solo PDF | Aggregati su Area C/B e sosta. Licenza non verificata |

**Open-Meteo:** termini ufficiali: API gratuita solo non commerciale, dati CC BY 4.0 con attribuzione. Per il rilascio commerciale serve piano a pagamento (D-004 analogo: decisione umana).

**OSM:** tag utili: `amenity=parking`, `parking=street_side|lane|surface|multi-storey`, `parking:lane:*` (`parking:left/right/both`, `:orientation`, `:fee`, `:capacity`), `access`, `fee`, `maxstay`, `capacity`, `amenity=parking_space`. Copertura a Milano: non misurata. Da quantificare via Overpass in un task (non in bulk dal servizio pubblico: usare estratto Geofabrik).

## Fonti in tempo reale (T-027, consultazione 2026-11-14)

Esito sintetico: **nessuna fonte pubblica fornisce l'occupazione degli stalli su strada a Milano.** Il segnale in tempo reale utilizzabile è indiretto (contesto: meteo, traffico, eventi, sharing, trasporto). Nessun account creato, nessun ente contattato. Stato: L = letta, S = secondaria (ricerca web), B = bloccata/non verificabile.

| Fonte | Endpoint / dove | Frequenza | Licenza / termini | Costo / accordo | Utilità per la sosta su strada | Stato |
|---|---|---|---|---|---|---|
| Posti liberi parcheggi interscambio/struttura ATM | Sito/app ATM (sez. Parcheggi) | Non noto | Non noto | Nessuna API pubblica trovata; servirebbe accordo (decisione fondatore) | Media: indica pressione sulla città (Lampugnano/Famagosta pieni 8-9:30, fonte guida) | S: live non confermato |
| Sensori smart parking ATM/Comune | Annuncio 2022 (ilgiorno.it) | n/d | n/d | Accordo | Alta se esistesse | S: non risulta operativo, nessun feed |
| Varchi Area C, transiti | ds82 (posizione), ds779+ (conteggi) | Mensile, in ritardo (ultimo nov. 2024) | CC BY 4.0 | Gratis | Bassa live; buona come prior orario/giorno (pressione ingressi) | L |
| BikeMi GBFS | `gbfs.urbansharing.com/bikemi.com/gbfs.json` (header `Client-Identifier`) | 10 s | Open data BikeMi (termini da leggere) | Gratis, senza chiave dichiarata | Media: stazioni piene/vuote = flussi in centro; proxy di attività | S: bloccato da qui, non testato |
| Monopattini/bici free-floating, car sharing | Nessun GBFS pubblico trovato | n/d | n/d | Operatori singoli | Media (veicoli parcheggiati) ma non reperibile; Comune ha 1 operatore monopattini (emTransit), flotta in cambiamento | S: non trovato |
| Traffico TomTom | Traffic Flow/Incidents API, developer.tomtom.com | Minuti | Freemium: 2.500 richieste non-tile al giorno, uso commerciale ammesso; clausole su cache/ML non lette | Gratis (chiave = account) | Media: congestione come proxy di domanda | S: leggere T&C prima di salvare dati |
| Traffico HERE | Traffic API, piano Base | Minuti | Quota gratuita ~5.000 transazioni/mese (fonti discordanti); divieto cache >30 giorni (termini Platform, non confermato per Traffic) | Gratis fino a soglia, poi a consumo | Come TomTom | S |
| Traffico Google | Routes API | Minuti | Vietato salvare/usare nel modello (D-004) | n/a | Esclusa | decisione già presa |
| Waze for Cities | Modulo di candidatura Waze | Quasi live | Scambio dati bidirezionale gratuito, ogni uso richiede approvazione, rivendita limitata | Accordo (solo per enti pubblici, non per noi) | Eventi/chiusure, dati utenti Waze | S: solo descritto, nessun contatto |
| GTFS-realtime ATM / Trenord | Non trovato | n/d | n/d | n/d | Bassa | S: statico sì (ds929 e dati.lombardia.it), realtime no |
| GTFS statico ATM | `dati.comune.milano.it/gtfs.zip` | Aggiornamento periodico (v425 al 2026-10-26) | CC BY 4.0 | Gratis | Bassa: accessibilità di quartiere, non live | L |
| Meteo Open-Meteo | `api.open-meteo.com` | Oraria | Dati CC BY 4.0; API gratuita solo non commerciale (<10.000 chiamate/giorno) | Beta chiusa non commerciale: gratis. Commercio: piano da circa 29 USD/mese (blog del fornitore, da riverificare) | Media: pioggia cambia la domanda di sosta | S |
| Meteo ARPA | Stazioni ARPA (ds699) | n/d | CC BY 4.0 (posizioni) | Gratis | Alternativa locale, serie live da verificare | L (solo anagrafica) |
| Scioperi | Calendario MIT/Commissione di Garanzia (RSS) | Giornaliera | Non verificata | Gratis | Bassa-media: sciopero mezzi = più auto | S |
| Eventi | ds2468 (Digital Week 2023) è l'unico visto; nessun calendario eventi live nel catalogo | n/d | CC BY 4.0 | n/d | Alta (stadio, fiere) ma fonte da trovare | L (ricerca "eventi") |

### Valutazione
Ordine di utilità/fattibilità per una beta: (1) segnalazioni degli utenti stessi (unica misura reale di occupazione, iterazione 2); (2) meteo (Open-Meteo, non commerciale in beta); (3) BikeMi GBFS (da testare quando il host è raggiungibile); (4) eventi e scioperi (calendario pubblico, da costruire); (5) traffico TomTom freemium (solo dopo lettura T&C su storage e ML).

Esclusi: Google (D-004); Waze (accordo richiesto, non per noi); posti liberi ATM e sensori (nessun feed pubblico, serve accordo con ente: decisione del fondatore).

### Da verificare [verificare]
- T&C TomTom e HERE su storage, cache e uso per addestrare modelli.
- Termini d'uso del feed GBFS BikeMi e raggiungibilità.
- Esistenza di feed GBFS/MDS di monopattini e car sharing.
- Tariffe per ambito: fonte ufficiale (non è nel catalogo).
- Perimetro Area B e calendario lavaggio strade (non nel catalogo).
- Calendario eventi pubblico e licenza dati scioperi.

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

## Strade di Milano: Database Topografico del Comune (fonte in uso, D-027)

- **Fonte:** dataset ds2889, "Database Topografico (DBT) 2020 - formato SHP", Comune di Milano, CC BY. Archivio da circa 600 MB su `gisportal.comune.milano.it`; si scaricano solo gli strati `EL_STR` (elementi stradali con nome) e `LIM_COM` (confine).
- **Comandi:** `scripts/fetch_city.py milano` poi `scripts/build_streets.py milano` → `build/streets/milano/streets.json` (circa 8 MB, fuori dal repository).
- **Esito del 2026-11-14:** 24.008 elementi, 30.727 tratti, 1.654 celle con strade, nome presente su tutti.
- **Ambiti della sosta:** dataset ds83 scaricato (36 ambiti con geometria). **I campi di tariffa, orari e numero di posti sono vuoti**: servono altre fonti (T-031).
- **Mancano:** attributi di sosta per tratto, stalli moto. Altri strati utili dello stesso archivio da valutare: `AC_VEI` (aree di circolazione veicolare), `AR_STR` (aree stradali).
- **Attribuzione nell'app:** "Comune di Milano, Database Topografico 2020 (CC BY 4.0)".

## OpenStreetMap (fonte di riserva e per altre città)

- `scripts/fetch_osm.py <città>` è pronto, ma dal 2026-11-14 la connessione a `overpass-api.de`, `overpass.kumi.systems` e `download.geofabrik.de` viene interrotta dalla rete della sessione anche se i siti sono abilitati.
- Scarico manuale possibile dal fondatore (gratis, senza account): `overpass-turbo.eu` con la richiesta contenuta nello script, poi "Esporta → dati grezzi"; il file va in `data/raw/<città>/osm_streets.json`.
- Licenza ODbL: attribuzione obbligatoria e vincoli sulla cessione di dati derivati (T-024).
