# 17 — Lavoro autonomo e definizione di "beta valida"

Deciso dal fondatore il 2026-11-14 (D-028): il team lavora anche senza richiesta, con la sessione principale nel ruolo di CEO.

## 1. Chi fa cosa
- **CEO (sessione principale o ciclo programmato):** sceglie i task, delega, integra, verifica, decide le priorità, riferisce al fondatore. Scrive codice solo quando delegare costerebbe di più.
- **Capi area:** `product-manager` (con `ux-designer`, `visual-designer`, `competitor-analyst`), `data-scientist` (con `data-engineer`), `backend-engineer` (con `mobile-engineer`, `qa-tester`), `privacy-compliance` (con `privacy-engineer`, `privacy-redteam`, `legal-analyst`), `release-manager`, `ops-watchdog`, `marketing-sales`.
- **Fondatore:** le decisioni di `CLAUDE.md` §7 e la direzione del prodotto.

## 2. Il ciclo (ogni giorno alle 03:41, e a ogni `vai`)
1. Leggere `STATO.md` e `TASKS.md`.
2. Scegliere i task **sbloccati** con priorità più alta che avvicinano alla beta valida (§4). Al massimo 4 deleghe per ciclo.
3. Prima di ogni ricerca web: provare un sito con `scripts/fetch_text.py`. Rete bloccata = non si delega la ricerca.
4. Delegare in parallelo con file non sovrapposti. Ogni delega: obiettivo, file, criteri, vincoli, budget, tetto di chiamate.
5. Integrare: `make check` e `make reid` verdi, altrimenti non si fa push.
6. Aggiornare `TASKS.md`, `STATO.md`, `14-valutazione-agenti.md` (un voto per agente usato).
7. Scrivere in `STATO.md` da 1 a 3 **proposte per il fondatore**, con costo e beneficio.
8. Commit, push, messaggio di massimo 120 parole.

## 3. Limiti
- Nessun account, spesa, pubblicazione, contatto esterno, firma: restano del fondatore.
- Veto di `privacy-compliance`: nessuna raccolta nuova senza il suo parere.
- Niente lavoro inventato: se nessun task è sbloccato, il ciclo lo scrive e si ferma.
- Costo: un ciclo con 4 deleghe consuma indicativamente da 300.000 a 600.000 token. Il fondatore può sospendere o diradare il ciclo quando vuole (attività programmata "App parcheggi - ciclo autonomo giornaliero").
- Due cicli consecutivi senza progresso misurabile: il ciclo successivo riduce le deleghe a 1 e lo segnala.

## 4. Definizione di "beta valida" (non una beta di base)
La beta è valida quando tutte le voci sono vere. Stato al 2026-11-14 tra parentesi.

**Dati e modello**
- [x] Strade reali di Milano collegate alle celle (30.727 tratti dal Database Topografico del Comune).
- [ ] Posti per strada: fatte le aree di sosta mappate (circa 123.000 posti stimati); manca la sosta lungo il marciapiede (D-030).
- [ ] Regole di sosta per strada: ambiti, orari, tariffe (ambiti scaricati; tariffe e orari senza fonte verificata).
- [x] Modello con componente "adesso", stime per altri orari, correzione per veicolo (valori provvisori).
- [ ] Stalli e regole per le moto.
- [ ] Dato reale visibile su tutto il Comune tramite la stima a livelli (D-029, T-045).

**Servizio**
- [ ] API che riceve gli eventi e pubblica la griglia ogni 5 minuti, in locale (in corso).
- [ ] Servizio raggiungibile dai tester su un piano gratuito. **Richiede un account creato dal fondatore.**

**App Android**
- [ ] Mappa reale con le strade colorate, vista live e altri orari.
- [ ] Scelta del veicolo, contributi a un tocco, "ricorda dove ho parcheggiato", timer.
- [ ] Rilevamento automatico sul telefono, spento in partenza.
- [ ] Italiano e inglese, funzionamento senza rete, schermate privacy e diritti.
- [ ] File dell'app installabile. **Richiede Flutter e Android SDK nell'ambiente (siti da abilitare) e una prova su un telefono vero, che può fare solo il fondatore.**

**Privacy e qualità**
- [x] Condizioni C1, C2, C6 nel codice con test.
- [ ] Tutti gli attacchi di re-identificazione superati, compresi quelli sul telefono e sul server.
- [ ] DPIA verificata sulle fonti. **Firma del fondatore dopo revisione di un professionista.**
- [ ] Nota informativa per i tester. **Approvazione del fondatore.**

**Persone**
- [ ] Tester reclutati su tutta la città: più sono, più la mappa è dettagliata. **Li trova il fondatore.**

## 5. Cosa può fare solo il fondatore, in ordine di urgenza
1. Abilitare i siti necessari quando arriva la richiesta (un tocco).
2. Creare l'account gratuito per il servizio, quando indicato quale.
3. Provare l'app su un telefono Android.
4. Far rivedere e firmare la DPIA.
5. Reclutare i tester.
