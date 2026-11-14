# 16 — Grafica

Stato: **prima bozza** (2026-11-14), non ancora provata su telefono né con utenti. Proprietario: `visual-designer`. Flussi e testi: [`08-ux.md`](08-ux.md).

## Dove vederla
- Tavole pubblicate (private, del fondatore): https://claude.ai/artifact/ChLZtfNZZvJ3Aji8uCQe6L
- Sorgente nel repository: `design/schermate/`

## Schermate disegnate
| Tavola | Contenuto |
|---|---|
| 1 · Mappa | Zone esagonali, ricerca, "Adesso" o orario di arrivo, scheda con una frase e "Portami lì" |
| 2 · Scheda zona | Verdetto, "circa 7 volte su 10", affidabilità, orari successivi, regole di sosta |
| 3 · La mia auto e contributo | Tre esiti a un tocco, auto salvata, timer, rilevamento automatico (spento in partenza) |
| 4 · Consenso | Spiegazione della posizione prima della richiesta di sistema |

Mancano: privacy e diritti, onboarding passi 1 e 3, stato senza rete, modalità scura, icona dell'app.

## Token (provvisori)
| Nome | Valore | Uso |
|---|---|---|
| ink | #14202B | Testo, selezione |
| ink-soft | #51606E | Testo secondario |
| ground | #F4F6F8 | Sfondo |
| surface | #FFFFFF | Schede |
| accent | #2251CC | Azione principale |
| level-high | #1FA68A (testo #0B6B57) | Facile: tinta piena, icona spunta |
| level-mid | #F2B632 (testo #7A4E00) | Possibile: tinta piena, icona trattino |
| level-low | #8E2A4B | Difficile: **tratteggio diagonale**, icona croce |
| level-unknown | #B4BDC6 | Dati insufficienti: **puntinato** |

Tipografia: Space Grotesk per titoli e verdetti, Inter per il resto (licenze aperte, da confermare prima del lancio). Raggi 16–24 px. Aree toccabili da 44 px.

## Scelte motivate
- **Verde acqua, ambra, rosso scuro** invece di verde, giallo, rosso puri: i tre livelli differiscono in luminosità e restano distinguibili per chi non vede il rosso e il verde. In più trama e icona.
- **Nessuna percentuale sulla mappa**: solo nella scheda zona, come frequenza ("7 volte su 10").
- **Segnaposto** per tariffe e lavaggio strade: la fonte ufficiale non è verificata (T-031).

## Da decidere con il fondatore
- Direzione generale (chiara e sobria, come nella bozza) e colore d'azione.
- Stile della mappa reale: la bozza usa una mappa stilizzata, non i tasselli veri.
