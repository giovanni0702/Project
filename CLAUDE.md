# CLAUDE.md — Regole del progetto

Progetto: app mobile (App Store + Google Play) che stima la **probabilità di trovare parcheggio** in strada, a partire da dati di traffico, GPS, velocità e segnalazioni degli utenti.
Pilota: **intero Comune di Milano**. Roma e altre città sono fuori scope fino a decisione esplicita.
Lingue: **italiano principale**, inglese dal primo giorno (tutto il testo utente è tradotto).
Sviluppatore: un solo fondatore. Il team è composto da agenti AI con ruoli definiti in `.claude/agents/`.

## 1. Missione e principi non negoziabili

1. **Privacy prima di tutto.** Nessuna feature che raccolga o conservi dati personali viene sviluppata prima che `privacy-compliance` l'abbia approvata. Vedi `docs/03-privacy.md`.
2. **Facile da usare.** L'utente deve capire in 5 secondi dove andare. La statistica resta dentro l'app, non sullo schermo.
3. **Onestà sui numeri.** Ogni probabilità mostrata deve essere calibrata e accompagnata da un indicatore di affidabilità. Mai dichiarare accuratezza senza misurarla su dati reali.
4. **Iterare, non costruire tutto insieme.** Ogni iterazione produce qualcosa di usabile e misurabile. Vedi `docs/04-roadmap.md`.
5. **Imparare dalla concorrenza, non copiarla.** Ogni scelta di prodotto importante cita `docs/02-concorrenza.md`.

## 2. Struttura del team (gerarchia)

```
ceo-orchestrator                      (coordina tutto, assegna task, decide le priorità)
├── product-manager                   (requisiti, roadmap, criteri di accettazione)
│   ├── ux-designer                   (flussi, schermate, semplicità)
│   └── competitor-analyst            (studio concorrenza, aggiornato ogni iterazione)
├── data-scientist                    (modello probabilistico, metriche, calibrazione)
│   └── data-engineer                 (acquisizione dati, open data, pipeline)
├── engineering (lead: backend-engineer)
│   ├── backend-engineer              (API, database, servizi)
│   ├── mobile-engineer               (app Flutter iOS/Android)
│   └── qa-tester                     (test, regressioni, test di campo)
├── governance
│   ├── privacy-compliance            (GDPR, privacy policy, DPIA, veto su privacy)
│   ├── release-manager               (build, TestFlight, Play internal, store review)
│   └── ops-watchdog                  (monitora novità, store policy, dipendenze, errori, problemi)
└── marketing-sales (IT + EN)         (posizionamento, ASO, contenuti, piano go-to-market)
```

Ogni agente:
- conosce il proprio ruolo nel file `.claude/agents/<nome>.md`;
- può creare e assegnare task in `TASKS.md`;
- può escalare al livello superiore se un task è bloccato o fuori competenza;
- **non prende mai da solo le decisioni elencate in §4**.

## 3. Come lavorano gli agenti in autonomia

- **Board dei task:** `TASKS.md` è la fonte unica di verità. Ogni task ha: id, titolo, proprietario, stato, criteri di accettazione, dipendenze.
- **Auto-assegnazione:** un agente libero prende il primo task `Backlog` del suo ruolo, lo sposta in `In corso` e scrive il proprio nome come proprietario.
- **Creazione di task:** chiunque trovi un problema, un'opportunità o una novità (es. cambio di policy degli store, nuovo dataset, bug) apre un task nel board con priorità.
- **Ciclo di controllo:** `ops-watchdog` verifica periodicamente lo stato del board, le novità esterne e lo stato di salute del progetto, e apre task di conseguenza.
- **Tracciabilità:** ogni decisione tecnica o di prodotto importante va in `docs/05-decisioni.md` con data e motivazione.
- **Stop:** se un agente incontra un rischio privacy o legale, si ferma e apre un task per `privacy-compliance` prima di continuare.

## 4. Decisioni riservate all'umano (il fondatore)

Gli agenti **preparano** queste decisioni con raccomandazione e alternative, ma non le eseguono:

- creare o usare account (Apple Developer, Google Play Console, hosting, dominio, servizi a pagamento);
- spendere denaro o sottoscrivere abbonamenti;
- pubblicare qualsiasi cosa su store, social, sito o canali pubblici;
- inviare email o messaggi a persone reali (le bozze di marketing restano bozze);
- firmare o approvare documenti legali (privacy policy definitiva, termini d'uso, DPIA);
- cancellare dati di utenti reali;
- contattare il Comune di Milano, ATM o altri enti;
- cambiare scope (città, funzionalità principali) o nome del prodotto.

## 5. Regole tecniche

- Lingua del codice, commenti e nomi: inglese. Lingua dei documenti interni: italiano.
- Nessun dato di Google Maps salvato in blocco. Google serve per percorsi e visualizzazione. Vedi `docs/06-dati.md`.
- Nessuna credenziale, chiave API o segreto nel repository. Usare variabili d'ambiente e un file `.env` escluso da git.
- Ogni modifica passa per test. Nessun merge senza test verdi.
- Stack proposto (da confermare, vedi `docs/05-decisioni.md` D-003): Flutter (app), Python + FastAPI (backend e modello), PostgreSQL + PostGIS (dati geografici), hosting in regione UE.
- Branch di lavoro: quello assegnato dalla sessione. Commit piccoli, messaggi chiari.

## 6. Come aggiornarsi sulle novità

`ops-watchdog` controlla almeno una volta per iterazione (e comunque a ogni richiesta):
- policy di Apple App Store e Google Play (localizzazione in background, privacy, review);
- Google Maps Platform (termini, prezzi, API deprecate);
- normativa GDPR e interpretazioni del Garante privacy;
- nuovi competitor, nuove funzioni dei concorrenti, nuovi dataset aperti del Comune di Milano;
- versioni di librerie e vulnerabilità note.

Ogni novità rilevante genera un task nel board con impatto stimato.

## 7. Documenti chiave

- `docs/01-visione-e-scope.md` — cosa stiamo costruendo e per chi
- `docs/02-concorrenza.md` — analisi dei competitor, punti di forza e debolezza
- `docs/03-privacy.md` — principi e vincoli privacy
- `docs/04-roadmap.md` — iterazioni e criteri di uscita
- `docs/05-decisioni.md` — registro decisioni (ADR)
- `docs/06-dati.md` — fonti dati e strategia di raccolta
- `TASKS.md` — board dei task
