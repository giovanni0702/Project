# STATO

Aggiornato: 2026-11-14 · Iterazione **1 — Dati e modello v0 (in corso)** · Lavoro autonomo attivo (D-028): ciclo ogni giorno alle 03:41, procedura in `17-autonomia.md`.

## Ultimi fatti
1. **Strade vere di Milano:** 30.727 tratti dal Database Topografico del Comune (D-027), collegati alle celle. Pagina di anteprima: https://claude.ai/artifact/VMEMf2xERBvgFQQ9Xz61F9 (`scripts/build_preview.py`).
2. **Backend:** `backend/` riceve gli eventi, pubblica griglia live e stime per altri orari, in locale.
3. **Red team:** 5 attacchi riusciti su 6 (`reports/reid/2026-11-14.md`). Correzione in corso (T-040). **Nessuna build va distribuita prima.**
4. **Beta con pochi tester:** con zone piccole e fasce da 30 minuti i dati reali non compaiono mai; proposta in `09-modello.md` §10.
5. **Legale:** elenco DPIA del Garante letto; testo del GDPR non raggiungibile (T-042). Bozza di nota per i tester in `18-nota-tester.md`.
6. Team: 17 agenti più 3 del team privacy e `visual-designer`; valutazioni in `14-valutazione-agenti.md`.

## Cosa sappiamo
- Nessuna fonte pubblica in tempo reale sulla sosta su strada a Milano: i dati reali sono solo i contributi dei tester.
- OpenStreetMap non è raggiungibile dalla sessione anche con i siti abilitati; Milano non ne ha bisogno per le strade.
- Mancano fonti verificate per tariffe, orari, lavaggio strade e stalli moto.

## Proposte per il fondatore
1. Beta in un quartiere solo (circa 3 km²): costo zero, è l'unico modo per vedere dati reali con 20 tester.
2. Usare gli strati `AC_VEI` e `AR_STR` del Database Topografico per stimare dove si può sostare: costo un ciclo di lavoro, toglie la dipendenza da OpenStreetMap.
3. Mostrare in app, per ogni strada, "quanto è recente il dato" al posto della sola affidabilità: costo basso, rende onesto il ritardo imposto dalla privacy.

## Prossimi passi
1. Chiudere T-040 e far ripetere gli attacchi al red team.
2. T-041 (attributi di sosta, moto), T-043 (app Android), T-044 (pagina interna sui dati del backend).
3. T-030 (server gratuito), T-031 (contesto in tempo reale), T-004 (concorrenti).

## Blocchi
- T-042: testi di legge non raggiungibili.
- Azioni del fondatore prima della beta: `17-autonomia.md` §5.
