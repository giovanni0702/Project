# STATO

Aggiornato: 2026-11-14 · Iterazione **1 — Dati e modello v0 (in corso)** · Iterazione 0 chiusa con conferma del fondatore.

## Ultimi fatti
1. Nucleo indipendente dalla città (`cities/milano`, `parking_core/`): modello, componente "adesso", taglia del veicolo (valori provvisori), griglia statica.
2. **Privacy nel codice (C1, C2, C6):** pseudonimo per cella, griglia a classi senza conteggi, ammissione a blocchi; `make reid` verde (attacchi A e B, dati sintetici).
3. **Strade (D-021):** `scripts/fetch_osm.py` e `scripts/build_streets.py` pronti; scarico reale da riprovare (siti OSM abilitati ma non ancora raggiungibili).
4. **Team privacy (D-025):** `privacy-engineer`, `privacy-redteam`, `legal-analyst` sotto `privacy-compliance`.
5. Grafica: direzione approvata (D-024), linee sottili e continue (D-026), 5 schermate in `docs/16-grafica.md`.
6. Decisioni recenti: D-018 con C1–C12, D-021 strade, D-022 live e stime, D-023 veicolo e moto.

## Cosa sappiamo
- **Nessuna fonte pubblica in tempo reale sull'occupazione della sosta su strada a Milano.** I dati reali sono solo i contributi dei tester.
- Il catalogo del Comune non ha stalli, sensori, tariffe né lavaggio strade.
- Beta Android gratuita fattibile con installazione diretta.
- Con pochi tester la soglia k non si raggiunge: problema aperto (T-029, R-20).

## Prossimi passi
1. Riprovare `scripts/fetch_osm.py milano`, poi `scripts/build_streets.py milano` e misurare la copertura (T-035).
2. T-038 (fonti legali), T-039 (attacchi nuovi), resto di T-034 (lato server).
3. T-010, T-029 (metriche, pochi tester), T-036 (veicolo e moto), T-037 (live e stime), T-030 (server gratuito).

## Blocchi
- Nessuno. Siti dei fornitori di hosting non ancora abilitati nella rete (T-030).
