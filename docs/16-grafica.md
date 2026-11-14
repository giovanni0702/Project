# 16 — Grafica

Stato: **direzione approvata dal fondatore il 2026-11-14 (D-024): mantenerla.** Seconda bozza, non ancora provata su telefono né con utenti. Proprietario: `visual-designer`. Flussi e testi: [`08-ux.md`](08-ux.md).

## Dove vederla
- Tavole pubblicate (private, del fondatore): https://claude.ai/artifact/ChLZtfNZZvJ3Aji8uCQe6L
- Sorgente nel repository: `design/schermate/`

## Schermate disegnate
| Tavola | Contenuto |
|---|---|
| 1 · Mappa delle strade | Ogni strada colorata per livello, "Live adesso" sempre attivo all'apertura, altro orario, veicolo |
| 2 · Scheda strada | Verdetto per il proprio veicolo, affidabilità, altri orari e giorni (stime), regole di sosta |
| 3 · Il mio veicolo | Ricerca del modello o scelta della taglia, moto comprese |
| 4 · Contributo e sosta | Tre esiti a un tocco, veicolo salvato, timer, rilevamento automatico (spento in partenza) |
| 5 · Consenso | Spiegazione della posizione prima della richiesta di sistema |

Mancano: privacy e diritti, onboarding passi 1 e 3, stato senza rete, modalità scura, icona dell'app, mappa reale al posto di quella stilizzata.

## Token (provvisori)
| Nome | Valore | Uso |
|---|---|---|
| ink | #14202B | Testo, selezione |
| ink-soft | #51606E | Testo secondario |
| ground | #F4F6F8 | Sfondo |
| surface | #FFFFFF | Schede |
| accent | #2251CC | Azione principale |
| level-high | #1FA68A (testo #0B6B57) | Facile: linea piena, icona spunta |
| level-mid | #E0A21A (testo #7A4E00) | Possibile: linea piena, icona trattino |
| level-low | #8E2A4B | Difficile: **linea tratteggiata**, icona croce |
| level-unknown | #7C8894 | Dati insufficienti: **linea puntinata** |

Tipografia: Space Grotesk per titoli e verdetti, Inter per il resto (licenze aperte, da confermare prima del lancio). Raggi 16–24 px. Aree toccabili da 44 px.

## Scelte motivate
- **Verde acqua, ambra, rosso scuro** invece di verde, giallo, rosso puri: i tre livelli differiscono in luminosità e restano distinguibili per chi non vede il rosso e il verde. In più trama e icona.
- **Nessuna percentuale sulla mappa**: solo nella scheda zona, come frequenza ("7 volte su 10").
- **Segnaposto** per tariffe e lavaggio strade: la fonte ufficiale non è verificata (T-031).

## Aperto
- Stile della mappa reale: la bozza usa una mappa stilizzata, non i tasselli veri (T-020, T-033).
- Etichetta della sezione: "La mia auto" diventa "Il mio veicolo" in tutte le tavole.
