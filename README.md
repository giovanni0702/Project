# App parcheggi — Milano

App mobile (iOS e Android) che stima la probabilità di trovare parcheggio in strada nel Comune di Milano.

Stato: **Iterazione 0 — fondamenta**. Non è ancora un prodotto utilizzabile.

## Da dove partire
- [`docs/STATO.md`](docs/STATO.md): dove siamo e cosa viene dopo
- [`TASKS.md`](TASKS.md): board dei task e decisioni richieste
- [`docs/INDICE.md`](docs/INDICE.md): cosa contiene ogni documento
- [`CLAUDE.md`](CLAUDE.md): regole del progetto e team di agenti

## Comandi in chat (per il fondatore)
| Comando | Effetto |
|---|---|
| `vai` | Legge lo stato e prosegue col prossimo passo |
| `stato` | Riassunto in 5 righe |
| `decido 1A 2B 3no` | Risponde alle decisioni numerate |
| `dettagli <tema>` | Approfondisce solo quel tema |
| `watchdog` | Ciclo di controllo su novità e salute del progetto |
| `chiudi` | Chiusura dell'iterazione |

Per spendere meno: una chat nuova per ogni task, iniziata con `vai`.

## Controlli
`make check` verifica lunghezza dei documenti, coerenza dei valori chiave e assenza di segreti.

## Principi
Privacy prima di tutto · semplicità per l'utente · onestà sui numeri · iterazioni misurabili.
