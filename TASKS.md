# TASKS.md — Board dei task

Fonte unica di verità per il lavoro degli agenti. Regole in `CLAUDE.md` §3.

## Formato di un task

```
### T-<id> — <titolo>
- Ruolo: <agente proprietario o "backlog" per ruolo>
- Stato: Backlog | In corso | Bloccato | Fatto
- Proprietario: <nome agente o vuoto>
- Priorità: alta | media | bassa
- Dipendenze: <id o nessuna>
- Criteri di accettazione:
  - [ ] ...
- Note:
```

## Backlog iniziale — Iterazione 0

### T-001 — Verificare il portale open data del Comune di Milano
- Ruolo: data-engineer
- Stato: Backlog
- Priorità: alta
- Criteri di accettazione:
  - [ ] Elenco dei dataset su sosta, zone, tariffe, parcheggi, con link e licenza
  - [ ] Esito chiaro: esiste o non esiste un dataset di stalli o sensori
  - [ ] Documento aggiornato in `docs/06-dati.md`

### T-002 — Verificare i termini ufficiali di Google Maps Platform
- Ruolo: privacy-compliance
- Stato: Backlog
- Priorità: alta
- Criteri di accettazione:
  - [ ] Testo ufficiale dei termini citato con data
  - [ ] Parere su caching, bulk, uso per modelli propri
  - [ ] Decisione D-004 confermata o aggiornata in `docs/05-decisioni.md`

### T-003 — Verificare i requisiti store per localizzazione in background
- Ruolo: release-manager
- Stato: Backlog
- Priorità: alta
- Criteri di accettazione:
  - [ ] Requisiti Apple App Store (linee guida 5.1.x) con link ufficiale
  - [ ] Requisiti Google Play per localizzazione in background con link ufficiale
  - [ ] Lista di cosa serve per la prima release, in `docs/03-privacy.md`

### T-004 — Approfondire i competitor sugli store
- Ruolo: competitor-analyst
- Stato: Backlog
- Priorità: alta
- Criteri di accettazione:
  - [ ] Verifica sugli store di EasyPark, FindPark, myCicero, Parkopedia, ParkEz, SpotGenius
  - [ ] Recensioni recenti (ultimi 12 mesi) con temi ricorrenti
  - [ ] Stato di "Find & Park" a Milano nel 2026
  - [ ] Tabella aggiornata in `docs/02-concorrenza.md`

### T-005 — Proposta di stack tecnico (conferma del fondatore)
- Ruolo: backend-engineer
- Stato: Backlog
- Priorità: media
- Dipendenze: nessuna
- Criteri di accettazione:
  - [ ] Confronto tra Flutter e React Native, con costi e rischi
  - [ ] Scelta hosting in regione UE con costo mensile stimato
  - [ ] Aggiornamento di D-003 in `docs/05-decisioni.md`

### T-006 — Scaffold del repository per l'iterazione 1
- Ruolo: backend-engineer
- Stato: Backlog
- Priorità: media
- Dipendenze: T-005
- Criteri di accettazione:
  - [ ] Struttura cartelle `backend/`, `model/`, `app/`, `docs/`
  - [ ] Test di base eseguibili
  - [ ] `.gitignore` con `.env` e dati locali

### T-007 — Primo ciclo di controllo novità e salute del progetto
- Ruolo: ops-watchdog
- Stato: Backlog
- Priorità: media
- Dipendenze: T-001, T-002, T-003, T-004
- Criteri di accettazione:
  - [ ] Report breve in `docs/07-report-watchdog.md` con novità, rischi e task aperti
  - [ ] Task creati per ogni rischio alto

### T-008 — Piano marketing e posizionamento (IT + EN)
- Ruolo: marketing-sales
- Stato: Backlog
- Priorità: media
- Dipendenze: T-004
- Criteri di accettazione:
  - [ ] Proposta di posizionamento, messaggio chiave e tre varianti di titolo IT/EN
  - [ ] Piano ASO iniziale (parole chiave, screenshot)
  - [ ] Nessuna azione esterna: solo bozze

### T-009 — Flusso utente e prime schermate (concept)
- Ruolo: ux-designer
- Stato: Backlog
- Priorità: media
- Dipendenze: T-004
- Criteri di accettazione:
  - [ ] Flusso di onboarding con consenso, mappa, "ho parcheggiato"
  - [ ] Test del flusso con 5 persone di prova (se il fondatore le organizza)
  - [ ] Documento in `docs/08-ux.md`

### T-010 — Definizione delle metriche di calibrazione
- Ruolo: data-scientist
- Stato: Backlog
- Priorità: alta
- Criteri di accettazione:
  - [ ] Definizione di calibrazione, Brier score e tolleranza
  - [ ] Metodo di test con dati sintetici etichettati
  - [ ] Documento in `docs/09-modello.md`

## In corso

_Nessun task._

## Bloccati

_Nessun task._

## Fatti

_Nessun task._
