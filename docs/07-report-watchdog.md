# 07 — Report watchdog

Si sovrascrive a ogni ciclo. Storico in git.

## Ciclo 1 — 2026-11-14

**Salute del progetto**
- `make check`: verde (limiti di lunghezza, descrizioni degli agenti, valori chiave coerenti, segreti).
- Nessun codice applicativo, nessuna dipendenza da controllare.
- Board: 4 task bloccati dalla rete, nessuno fermo da più di un'iterazione.

**Novità esterne** (dettagli e stato di ogni fonte in [`fonti.md`](fonti.md))
| Novità | Impatto | Azione |
|---|---|---|
| Molti siti ufficiali non raggiungibili dalla sessione | Alto: verifiche incomplete | Decisione 1 in `TASKS.md` |
| Nessun dataset aperto di stalli o sensori | Alto: il modello parte da proxy e contributi | R-03; T-021 |
| Apple: consenso anche per dati anonimi | Medio: onboarding | T-009, T-018 |
| Open-Meteo: API gratuita solo non commerciale | Medio | Usare i dati con licenza, non l'API gratuita; T-001 |
| GTFS ATM con validità forse scaduta | Basso | T-001 |
| Google Play: target API 36 | Basso | `10-release.md` |
| DSA: contatti del venditore pubblici sugli store | Medio per il fondatore (indirizzo e telefono visibili) | T-002; da decidere prima dell'iterazione 3 |
| Prezzi dell'hosting in aumento nel 2026 | Basso | Riverificare prima di attivare |

**Contraddizioni tra documenti:** nessuna rilevata dallo script. `01-visione-e-scope.md` non cita ancora le funzioni T-011–T-017: da allineare quando `product-manager` le conferma.

**Decisioni richieste:** vedi `TASKS.md`.
