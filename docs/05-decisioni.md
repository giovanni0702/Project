# 05 — Registro delle decisioni (ADR)

Formato: ogni decisione ha data, stato, contesto, scelta e conseguenze. Le decisioni "proposte" vanno confermate dal fondatore.

---

## D-001 — Scope geografico: intero Comune di Milano
- **Data:** 2026-11-14
- **Stato:** approvata
- **Contesto:** il fondatore vuole Milano come pilota completo, incluso il Comune.
- **Scelta:** l'area è tutto il territorio comunale di Milano. Roma e altre città sono fuori scope.
- **Conseguenze:** la copertura dati va pianificata su una griglia dell'intera città. La priorità di calibrazione è il centro.

## D-002 — Lingue: italiano principale, inglese dal lancio
- **Data:** 2026-11-14
- **Stato:** approvata
- **Scelta:** tutto il testo utente è internazionalizzato (IT primario, EN). Documenti interni in italiano, codice in inglese.
- **Conseguenze:** nessuna stringa hard-coded nell'interfaccia. Store listing in entrambe le lingue.

## D-003 — Stack tecnico (proposto)
- **Data:** 2026-11-14
- **Stato:** **proposta, da confermare**
- **Contesto:** un solo fondatore, con agenti AI. Serve una base unica per iOS e Android, con buon supporto a mappe e dati geografici.
- **Proposta:**
  - App: **Flutter** (un'unica codebase, buon supporto a localizzazione e mappe).
  - Backend: **Python + FastAPI**.
  - Modello: **Python** (pandas, NumPy, SciPy, statsmodels; PyMC se serve inferenza bayesiana avanzata).
  - Dati geografici: **PostgreSQL + PostGIS**, griglia **H3**.
  - Hosting: regione UE (da scegliere tra provider con piani economici).
- **Alternative:** React Native (se si preferisce JavaScript), backend Node.js, Firebase/Supabase come BaaS.
- **Da confermare:** scelta del fondatore, budget hosting.

## D-004 — Google Maps: solo percorsi e visualizzazione
- **Data:** 2026-11-14
- **Stato:** approvata in principio, da verificare con i termini attuali
- **Contesto:** i termini di Google Maps Platform limitano il caching e il download in blocco dei dati. La ricerca ha trovato solo fonti secondarie.
- **Scelta:** Google Maps serve per percorsi, navigazione e visualizzazione. Non salviamo in blocco dati Google. Il modello usa dati nostri (eventi utenti, open data, OSM).
- **Conseguenze:** `privacy-compliance` e `data-engineer` verificano i termini ufficiali prima della iterazione 1. Se necessario, si valutano alternative (HERE, TomTom, Mapbox) solo per il traffico.

## D-005 — Privacy by design
- **Data:** 2026-11-14
- **Stato:** approvata
- **Scelta:** vedi `03-privacy.md`. Nessuna traccia GPS grezza sul server. Aggregazione con soglia k. Nessun video.
- **Conseguenze:** la raccolta è più povera di dati, ma più solida. Il modello deve funzionare con pochi eventi per cella.

## D-006 — Decisioni riservate al fondatore
- **Data:** 2026-11-14
- **Stato:** approvata
- **Scelta:** gli agenti non creano account, non spendono, non pubblicano, non firmano documenti legali e non contattano persone o enti esterni. Vedi `CLAUDE.md` §4.

## D-007 — Lavoro a iterazioni
- **Data:** 2026-11-14
- **Stato:** approvata
- **Scelta:** iterazioni 0–4 come da `04-roadmap.md`. Il prodotto completo non è l'output della prima iterazione.
