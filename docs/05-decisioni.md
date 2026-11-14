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

## D-003 — Stack tecnico
- **Data:** 2026-11-14
- **Stato:** **proposta, da confermare dal fondatore**
- **Scelta:** app **Flutter**; backend **Python + FastAPI** con contratto OpenAPI come fonte unica; modello in Python (pandas, NumPy, SciPy, statsmodels; PyMC solo se serve); **PostgreSQL + PostGIS**, griglia **H3**; hosting UE.
- **Hosting raccomandato:** un server virtuale in UE (es. Hetzner) con tutto in Docker, più archivio statico con CDN (es. Cloudflare R2) per griglia e tasselli. Stima **5–15 €/mese fino a 10.000 utenti** **[verificare]**: prezzi presi da fonti secondarie, da rileggere sulle pagine ufficiali prima di attivare (→ `fonti.md`).
- **Alternative:** Postgres gestito (Neon, Supabase): gratuito all'inizio ma a consumo e con PostGIS e regione UE da verificare. Fly.io: prezzi non verificati. React Native: nessun vantaggio strutturale su mappe e localizzazione.
- **Conseguenze:** backup e manutenzione del server a nostro carico; nessuna fattura a consumo.

## D-004 — Nessun dato Google nel modello
- **Data:** 2026-11-14 (aggiornata dopo T-002)
- **Stato:** approvata in principio; testo corrente dei termini ancora **[verificare]**
- **Contesto:** i termini di servizio specifici (versione archiviata del 22/05/2024) consentono solo cache temporanea e vietano l'uso di alcuni contenuti con mappe non Google. Il testo corrente non è stato raggiungibile.
- **Scelta:** nessun dato Google viene salvato o usato come input del modello. Google Maps, Apple Maps e Waze si aprono solo tramite deep link per la navigazione.
- **Conseguenze:** il modello usa eventi propri, open data e OSM. Prima della release serve rileggere i termini correnti e i requisiti dei deep link.

## D-005 — Privacy by design
- **Data:** 2026-11-14
- **Stato:** approvata
- **Scelta:** vedi `03-privacy.md`. Nessuna traccia GPS grezza sul server. Aggregazione con soglia k. Nessun video.
- **Conseguenze:** la raccolta è più povera di dati, ma più solida. Il modello deve funzionare con pochi eventi per cella.

## D-006 — Decisioni riservate al fondatore
- **Data:** 2026-11-14
- **Stato:** approvata
- **Scelta:** gli agenti non creano account, non spendono, non pubblicano, non firmano documenti legali e non contattano persone o enti esterni. Vedi `CLAUDE.md` §7.

## D-007 — Lavoro a iterazioni
- **Data:** 2026-11-14
- **Stato:** approvata
- **Scelta:** iterazioni 0–4 come da `04-roadmap.md`. Il prodotto completo non è l'output della prima iterazione.

## D-008 — Modelli assegnati agli agenti
- **Data:** 2026-11-14
- **Stato:** approvata (reversibile)
- **Scelta:** modello più potente per `ceo-orchestrator`, `data-scientist`, `privacy-compliance` (errori costosi, lavoro raro); intermedio per chi scrive codice, requisiti e schermate; il più economico per ricerca e monitoraggio (`competitor-analyst`, `ops-watchdog`, `release-manager`, `marketing-sales`).
- **Conseguenze:** se un ruolo economico produce lavoro insufficiente, si alza di un livello e si annota qui.

## D-009 — Architettura del contesto per risparmiare token
- **Data:** 2026-11-14
- **Stato:** approvata
- **Scelta:** `CLAUDE.md` ≤ 100 righe; `STATO.md` come passaggio di consegne; `INDICE.md` per scegliere cosa leggere; `fonti.md` come cache delle ricerche; limiti di lunghezza verificati da `make check`; una sessione per task.

## D-010 — Mappa: MapLibre con dati OpenStreetMap
- **Data:** 2026-11-14
- **Stato:** **proposta, da confermare** dopo la prova tecnica T-020
- **Contesto:** la mappa di Google non ha un tetto di spesa automatico e porta vincoli sui termini; un fornitore di tasselli commerciale costa da circa 25 $/mese **[verificare]**.
- **Scelta proposta:** MapLibre con tasselli vettoriali OSM della sola area di Milano (PMTiles) serviti come file statico. Attribuzione ODbL obbligatoria.
- **Rischio:** maturità del pacchetto MapLibre per Flutter non verificata. Ripiego: fornitore di tasselli UE oppure Google Maps.

## D-011 — Pubblicazione statica della griglia
- **Data:** 2026-11-14
- **Stato:** approvata in principio
- **Scelta:** un job periodico calcola la griglia e la scrive come file statico su CDN. L'app la scarica intera. L'API serve solo a ricevere eventi.
- **Motivo:** il server non conosce la zona che l'utente guarda; costo quasi nullo; funzionamento offline.

## D-012 — Scala dei modelli e bersaglio osservabile
- **Data:** 2026-11-14
- **Stato:** approvata in principio
- **Scelta:** il bersaglio è "posto trovato entro 5 minuti, sì o no". Si parte da baseline e Beta-Binomiale gerarchico; il modello a tassi si adotta solo se li batte su dati reali. Dettagli in `09-modello.md`.
- **Motivo:** la formula 1 − e^(−λt) ignora concorrenza tra automobilisti e penetrazione dell'app.
