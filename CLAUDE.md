# CLAUDE.md — Regole del progetto

App mobile (iOS + Android) che stima la **probabilità di trovare parcheggio in strada** nel **Comune di Milano**. Italiano principale, inglese dal primo giorno. Un solo fondatore; il team è fatto di agenti AI (`.claude/agents/`).
Questo file è caricato a ogni turno: **massimo 100 righe, si modifica raramente**. I dettagli stanno nei documenti collegati.

## 1. Principi non negoziabili
1. **Privacy prima di tutto.** Nessuna raccolta di dati senza approvazione di `privacy-compliance` → `docs/03-privacy.md`.
2. **Facile.** Si capisce dove andare in 5 secondi. Niente statistica nella schermata principale.
3. **Onestà sui numeri.** Probabilità calibrate, affidabilità esplicita. I dati sintetici testano il codice, mai l'accuratezza → `docs/09-modello.md`.
4. **Iterare.** Ogni iterazione ha criteri di uscita e di abbandono → `docs/04-roadmap.md`.
5. **Imparare dalla concorrenza, non copiarla** → `docs/02-concorrenza.md`.
6. **Costo minimo.** Opzione gratuita o più economica; stima mensile prima di qualsiasi spesa.
7. **Accessibilità.** Mai informazione affidata al solo colore.

## 2. Inizio e fine sessione
- **Inizio:** leggi `docs/STATO.md` (40 righe). Scegli cosa altro leggere da `docs/INDICE.md`, non aprendo i file.
- **Fine:** aggiorna `docs/STATO.md` e `TASKS.md`. Suggerisci una chat nuova per il task successivo.

## 3. Efficienza dei token (vincolante per tutti gli agenti)
1. Glob/Grep prima di Read; Read con `offset`/`limit`. Non rileggere ciò che hai appena scritto.
2. Edit per modificare, Write solo per file nuovi.
3. Un fatto vive in un solo file; altrove link. Documenti ≤ 300 righe, `TASKS.md` ≤ 150, `STATO.md` ≤ 40.
4. Chiamate indipendenti nello stesso blocco.
5. Prima di una ricerca web: Grep in `docs/fonti.md`. Dopo: aggiungi una riga lì. Modalità extended solo per fonti ufficiali difficili.
6. Sub-agenti solo per lavoro parallelo o contesto separato. Delega = obiettivo, file, criteri, vincoli, budget. Mai documenti copiati.
7. **Report di un agente ≤ 150 parole:** esito, file toccati, task aperti, decisioni richieste. Output lungo in un file.
8. `make check` dopo ogni modifica (silenzioso: stampa solo i fallimenti). Suite completa solo a chiusura di iterazione.
9. Script per ogni operazione ripetuta (`scripts/`).
10. Budget del task superato, o due tentativi falliti sulla stessa strada: stop, stato nel task, follow-up.

## 4. Chat con il fondatore
- Risposta ≤ 120 parole: riga 1 stato (se bloccato, lo dice); poi Fatto / Aperto / Decisioni richieste (numerate, opzioni A/B, raccomandazione). Solo percorsi di file, mai contenuti.
- Domande raggruppate, una volta, con default. Sulle scelte reversibili si procede col default.
- Comandi: `vai` (prosegui da STATO) · `stato` · `decido 1A 2B` · `dettagli <tema>` · `watchdog` · `chiudi` (chiusura iterazione).

## 5. Team
```
ceo-orchestrator            pianifica, assegna, risolve conflitti; non scrive codice
├── product-manager         requisiti, roadmap, criteri
│   ├── ux-designer         flussi, testi IT/EN, accessibilità
│   └── competitor-analyst  concorrenza
├── data-scientist          modello, calibrazione, metriche
│   └── data-engineer       fonti, licenze, pipeline
├── backend-engineer        lead engineering: API, database, sicurezza
│   ├── mobile-engineer     app Flutter
│   └── qa-tester           test, test di privacy, test sul campo
├── privacy-compliance      GDPR, DPIA, VETO sulla raccolta dati
├── release-manager         build, store
├── ops-watchdog            novità esterne, salute del progetto
└── marketing-sales         posizionamento, ASO, sole bozze
```

## 6. Autonomia
- `TASKS.md` è la fonte unica di verità. Un agente libero prende il primo `Backlog` del proprio ruolo e lo segna `In corso`. Chiunque può aprire task.
- **"Fatto" significa:** criteri soddisfatti, `make check` verde, documento di riferimento aggiornato, riga in `docs/STATO.md`.
- Revisione incrociata solo qui: flussi di dati → `privacy-compliance`; modello → `qa-tester` riesegue le metriche.
- Decisioni tecniche o di prodotto importanti → `docs/05-decisioni.md`, con data e motivo. Non si ridiscutono in chat.
- Rischio privacy o legale: stop e task per `privacy-compliance`.
- `ops-watchdog` scrive `docs/07-report-watchdog.md` a ogni ciclo e apre task.

## 7. Decisioni riservate al fondatore
Gli agenti preparano (raccomandazione, alternative, costo) nella sezione "Decisioni richieste" di `TASKS.md` e si fermano:
- creare o usare account; spendere denaro; pubblicare qualsiasi cosa;
- inviare messaggi a persone o enti reali (le bozze restano bozze);
- firmare o approvare documenti legali (privacy policy, termini, DPIA);
- cancellare dati di utenti reali;
- contattare Comune di Milano, ATM o altri enti;
- cambiare scope, nome del prodotto o modello di ricavo.

## 8. Regole tecniche
- Codice, commenti e nomi in inglese. Documenti interni in italiano.
- Nessun segreto nel repository: variabili d'ambiente e `.env` escluso da git.
- Il server non riceve mai coordinate: solo cella H3 e fascia oraria.
- Nessun dato Google salvato o usato nel modello → `docs/05-decisioni.md`.
- Ogni modifica passa per test. Nessun merge senza `make check` verde.
- Stack e motivazioni → `docs/05-decisioni.md`.
- Branch: quello assegnato dalla sessione. Commit piccoli, messaggi chiari.
