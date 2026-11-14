# STATO

Aggiornato: 2026-11-14 · Iterazione **1 — Dati e modello v0 (in corso)** · Lavoro autonomo (D-032): martedì e venerdì alle 03:41 in una sessione dedicata, procedura in `17-autonomia.md`.

## Ultimi fatti
1. **Strade vere di Milano:** 30.727 tratti dal Database Topografico del Comune (D-027). Anteprima: https://claude.ai/artifact/VMEMf2xERBvgFQQ9Xz61F9.
2. **Posti (D-030, D-031):** 3.090 aree di sosta mappate (circa 123.000 posti stimati) e 74 parcheggi in struttura (circa 29.000 posti); mancano sosta lungo il marciapiede, tariffe e orari (T-041).
3. **Backend** in `backend/`: eventi, griglia live, stime per altri orari, in locale.
4. **Privacy:** 5 falle trovate dal red team e chiuse da `privacy-engineer` (T-040); `make check` e `make reid` verdi (75 test). Serve la verifica indipendente (T-047) prima di distribuire.
5. **Beta su tutto il Comune (D-029):** stima a livelli da costruire (T-045).
6. **Marketing:** piano di reclutamento, ganci e nomi in `11-marketing.md` (bozze).
7. Valutazioni degli agenti in `14-valutazione-agenti.md`.

## Cosa sappiamo
- Nessuna fonte pubblica in tempo reale sulla sosta su strada a Milano: i dati reali sono solo i contributi dei tester.
- OpenStreetMap non è raggiungibile dalla sessione anche con i siti abilitati; Milano non ne ha bisogno per le strade.
- Mancano fonti verificate per tariffe, orari, lavaggio strade e stalli moto.

## Proposte per il fondatore
1. Reclutare molti più di 20 tester (fino al 2027 l'installazione diretta non ha limiti di dispositivi): costo zero in denaro, è la leva principale per il dettaglio su tutta la città.
2. Usare gli strati `AC_VEI` e `AR_STR` del Database Topografico per stimare dove si può sostare: costo un ciclo di lavoro, toglie la dipendenza da OpenStreetMap.
3. Mostrare in app, per ogni strada, "quanto è recente il dato" al posto della sola affidabilità: costo basso, rende onesto il ritardo imposto dalla privacy.

## Prossimi passi
1. T-047 (verifica indipendente del red team), poi T-045 (stima a livelli).
2. T-041 (attributi di sosta, moto), T-043 (app Android), T-044 (pagina interna sui dati del backend).
3. T-030 (server gratuito), T-031 (contesto in tempo reale), T-004 (concorrenti).

## Blocchi
- T-042: testi di legge non raggiungibili.
- Azioni del fondatore prima della beta: `17-autonomia.md` §5.
