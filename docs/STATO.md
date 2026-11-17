# STATO

Aggiornato: 2026-11-17 · Iterazione **1 (in corso)** · Cicli autonomi: martedì e venerdì alle 03:41 in una sessione dedicata (D-032), procedura in `17-autonomia.md`.

## Ultimi fatti
1. **SostaMi versione web** (D-035, D-036): mappa vera di Milano dai dati del Comune, ricerca vie, veicolo, sosta salvata, segnalazioni sul dispositivo, "Dove sono". Privata: https://claude.ai/artifact/RCK6XaPgv7oTuTKun7Wk87. Sito pronto in `site/`, da pubblicare da un repository separato (D-038).
2. **Modello di occupazione** (D-037, `09-modello.md` §11): posti totali, occupati, liberi e probabilità per zona e fascia, con intervalli; collegato alla mappa. Corretto il 2026-11-17: il centro non è più facile (Brera feriale ore 11 da circa 100% a 45%). **Resta non verificato**: nessuna fonte esterna (T-050, `reports/t050-occupazione.md`).
3. **Dati:** 30.727 tratti di strada, 3.090 aree di sosta, 74 parcheggi in struttura, edifici, verde, acqua (Database Topografico del Comune, CC BY). Capacità stimata: circa 386.000 posti auto (290.000–448.000).
4. **Backend** in `backend/` (locale). **Privacy:** 5 falle chiuse (T-040). Verifica indipendente fatta (T-047): riescono ancora 3 attacchi (residuo live, casa/lavoro, conoscenza esterna) → T-051, T-052; **raccolta live ferma**.
5. Nome SostaMi e logo (D-033, marchio da verificare T-048); grafica in `16-grafica.md`; marketing in `11-marketing.md`.
6. Beta su tutto il Comune (D-029): stima a livelli da costruire (T-045).

## Cosa sappiamo
- Nessuna fonte pubblica in tempo reale sulla sosta su strada; i dati di Google non si possono usare (D-004, D-037).
- OpenStreetMap non raggiungibile dalla sessione; Milano usa i dati del Comune.
- Mancano fonti per tariffe, orari, lavaggio strade, stalli moto reali.

## Proposte per il fondatore
1. Conteggi su 20 tratti con il protocollo pronto (un'ora, costo zero): unica verifica del modello possibile prima della beta.
2. Abilitare nella rete `uibm.mise.gov.it`, `euipo.europa.eu`, `amat-mi.it` (un tocco): sblocca la verifica del nome e una fonte esterna per il modello.
3. "Adesso" aggiornato ogni 30 minuti invece di 5 (nessun costo, dato meno fresco): chiude subito il residuo privacy se l'opzione B non regge.

## Prossimi passi
1. Azioni del fondatore per pubblicare il sito (D-038); poi copia di `site/` e verifica.
2. T-051 (residuo live), T-053 (metriche rieseguite da qa-tester), T-045 (stima a livelli).
3. T-052, T-044 (dopo T-051), T-041, T-030.

## Blocchi
- Pubblicazione del sito: 4 azioni del fondatore. T-042 e T-048: siti di legge e registri marchi non raggiungibili.
