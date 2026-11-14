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
| **Comune di Milano — Open Data** (portale ufficiale) | Possibili dataset su sosta, zone, eventi, mobilità | Open data (verificare licenza per ogni dataset) | Da cercare sul portale ufficiale. Non confermato: stalli o sensori |
| **ATM / Sosta Milano** (gestore della sosta per il Comune) | Zone, tariffe, orari strisce blu | Da verificare | Da contattare solo su decisione del fondatore |
| **OpenStreetMap** | Rete stradale, parcheggi, POI | ODbL (attribuzione obbligatoria, share-alike sui dati derivati) | Utilizzabile, da documentare |
| **ISTAT** | Popolazione, densità, residenza | Open data | Utilizzabile |
| **Google Routes / Maps Platform** | Percorsi, navigazione, visualizzazione | Termini restrittivi su caching e bulk | Solo percorsi e visualizzazione (D-004) |
| **Eventi della città** (portale Comune o fonti pubbliche) | Eventi che cambiano la domanda di sosta | Da verificare | Da valutare |
| **Dati degli utenti** | Eventi anonimi di partenza e segnalazioni | Consenso dell'utente (vedi `03-privacy.md`) | Dalla iterazione 2 |

**Nota:** ricerche preliminari non hanno trovato, nei risultati, un dataset pubblico di sensori o stalli per le strisce blu di Milano. Il `data-engineer` deve verificarlo direttamente sul portale ufficiale e documentare il risultato.

## Stime di partenza da verificare
- Le stime sul numero di stalli su strada a Milano variano nella stampa (ordine di centinaia di migliaia). Non usarle come dato di input senza una fonte ufficiale.
- Il numero di sanzioni per sosta irregolare (2026) è riportato dalla stampa. Da verificare prima di citarlo in materiale pubblico.

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
