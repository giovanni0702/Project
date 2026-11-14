# STATO

Aggiornato: 2026-11-14 · Iterazione **1 — Dati e modello v0 (in corso)** · Iterazione 0 chiusa con conferma del fondatore.

## Ultimi fatti
1. Nucleo indipendente dalla città: `cities/milano/city.yaml`, `parking_core/` (griglia H3, fasce, modello Beta-Binomiale con soglia k, metriche), 12 test su dati sintetici in `make check`.
2. Testi ufficiali letti: termini Google (D-004 confermata), Google Play, verifica sviluppatore Android, ODbL, catalogo del Comune.
3. Decisioni: beta solo Android a costo zero (D-017); beta su dati reali e attuali (D-016); nessuna spesa fino al lancio (D-014); nessuna rilevazione sul campo (D-015); visione multi-città (D-013).
4. `scripts/fetch_text.py` legge i siti consentiti quando WebFetch non li raggiunge.

## Cosa sappiamo
- **Nessuna fonte pubblica in tempo reale sull'occupazione della sosta su strada a Milano.** I dati reali sono solo i contributi dei tester.
- Il catalogo del Comune non ha stalli, sensori, tariffe né lavaggio strade.
- Beta Android gratuita fattibile con installazione diretta.
- Con pochi tester la soglia k non si raggiunge: problema aperto (T-029, R-20).

## Prossimi passi
1. T-026: adattatore OSM (strade e sosta) e confine comunale; poi pubblicazione statica della griglia e pagina interna.
2. T-010 e T-029 (metriche, soglia k in beta); T-018 e T-028 (parere privacy, DPIA).
3. T-030 (server gratuito), T-031 (contesto in tempo reale), T-004 (concorrenti sugli store).

## Blocchi
- Nessuno. Siti dei fornitori di hosting non ancora abilitati nella rete (T-030).
