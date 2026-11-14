# TASKS.md — Board dei task

Fonte unica di verità. Regole in `CLAUDE.md` §6. Massimo 150 righe: i task `Fatto` passano in `docs/archivio/` a chiusura di iterazione.

Formato: `### T-id — titolo` · riga `Ruolo | Stato | Priorità | Budget (S/M/L) | Dipendenze` · `Criteri:` · `Note:` (facoltativa).
Stati: Backlog · In corso (con nome del proprietario) · Bloccato · Fatto.

## Decisioni richieste al fondatore

Nessuna urgente. Decise il 2026-11-14: D-003, D-010, D-013–D-017 (`docs/05-decisioni.md`).

1. **Prima della beta (non ora):** creare un account gratuito per il server della beta, quando T-030 avrà indicato quale. Lo crei tu.

## Iterazione 1 — in corso

### T-028 — DPIA e progetto del rilevamento via Bluetooth
privacy-compliance | Backlog | alta | L | T-018
Criteri: [ ] bozza di DPIA per tap, "ricorda dove ho parcheggiato" e Bluetooth · [ ] condizioni: consenso separato, scelta dell'auto, zone escluse sul dispositivo, nessun identificativo Bluetooth inviato · [ ] effetto sulla dichiarazione di posizione in background · [ ] pronta per la firma del fondatore

### T-029 — Dati reali visibili con pochi tester (soglia k) e piano di validazione
data-scientist | Backlog | alta | M | T-010
Criteri: [ ] stima di quanti esiti servono per superare k con 10–20 tester · [ ] proposta per la beta: zone, dimensione delle celle, larghezza delle fasce · [ ] missioni di copertura · [ ] quota di esiti riservata alla validazione · [ ] parere di `privacy-compliance`

### T-030 — Server gratuito per la beta
backend-engineer | Backlog | media | S | —
Criteri: [ ] pagine ufficiali lette (regione UE, PostGIS, carta richiesta, sospensione) · [ ] una combinazione raccomandata e un ripiego · [ ] host da abilitare nella rete elencati

### T-031 — Variabili di contesto in tempo reale
data-engineer | Backlog | media | M | T-026
Criteri: [ ] meteo con licenza adatta all'uso commerciale · [ ] scioperi ed eventi · [ ] BikeMi GBFS provato · [ ] termini TomTom letti (conservazione, uso in modelli) · [ ] fonte ufficiale di tariffe e lavaggio strade (assenti dal catalogo)

## Verifiche residue

### T-004 — Concorrenti sugli store
competitor-analyst | Backlog (usare `scripts/fetch_text.py`) | alta | M | —
Criteri: [x] `docs/02-concorrenza.md` aggiornato da fonti web · [ ] recensioni sugli store · [ ] Find & Park in app a Milano · [ ] SpotAngels e PuliAMO in Italia

## Backlog — prodotto (le 7 idee)

### T-011 — Regole della zona e avviso lavaggio strade
product-manager | Backlog | alta | M | T-031
Criteri: [ ] requisiti e criteri di accettazione · [ ] fonte dati verificata e data della fonte visibile · [ ] avviso "vale la segnaletica" · [ ] riferimento a `02-concorrenza.md`

### T-012 — "Ricorda dove ho parcheggiato" e timer di scadenza
product-manager | Backlog | alta | M | T-018
Criteri: [ ] tutto sul dispositivo · [ ] salvare l'auto propone l'evento "ho parcheggiato", ripartire "ho lasciato", con consenso · [ ] parere di `privacy-compliance`

### T-013 — "Piano B": zona verde vicina, strutture, interscambio
product-manager | Backlog | bassa | S | —
Criteri: [ ] requisiti per l'iterazione 4 · [ ] fonti dei parcheggi di struttura verificate

### T-014 — Sicurezza alla guida
ux-designer | Backlog | alta | S | —
Criteri: [ ] nessuna interazione richiesta in movimento · [ ] richieste di contributo solo a veicolo fermo · [ ] schermata leggibile in un colpo d'occhio · [ ] norma del Codice della Strada verificata · [ ] regole in `docs/08-ux.md`

### T-015 — Contatore locale "hai aiutato N automobilisti"
ux-designer | Backlog | bassa | S | T-012
Criteri: [ ] calcolo solo sul dispositivo · [ ] testi IT/EN · [ ] nessuna classifica, nessun profilo

### T-016 — Funzionamento offline
mobile-engineer | Backlog | media | M | T-020
Criteri: [ ] griglia e regole in cache · [ ] età della stima sempre visibile · [ ] invio differito dei contributi

### T-017 — Opzioni di ricavo (3 alternative, senza pubblicità)
marketing-sales | Backlog | bassa | S | T-004
Criteri: [ ] include il dato in licenza a terzi (D-013) · [ ] pro, contro e vincoli privacy per ciascuna in `docs/11-marketing.md` · [ ] raccomandazione · [ ] decisione lasciata al fondatore, non prima dell'iterazione 3

## Backlog — privacy, sicurezza, tecnica

### T-018 — Parere sui vincoli tecnici v2 e test di re-identificazione
privacy-compliance | Backlog | alta | M | —
Criteri: [ ] ogni vincolo di `docs/03-privacy.md` "Vincoli tecnici (v2)" approvato o corretto · [ ] rotazione dell'identificatore e diritti motivati · [ ] specifica del test di re-identificazione · [ ] indice della DPIA

### T-019 — Modello delle minacce e antiabuso
backend-engineer | Backlog | media | M | T-018
Criteri: [ ] `docs/12-sicurezza.md` completato · [ ] limiti di frequenza e controlli di plausibilità definiti · [ ] attestazione del dispositivo valutata con `privacy-compliance`

### T-020 — Prova tecnica della mappa (MapLibre + PMTiles in Flutter)
mobile-engineer | Backlog | alta | M | —
Criteri: [ ] mappa dietro un'interfaccia unica, sostituibile con Google Maps (D-010) · [ ] maturità del pacchetto verificata · [ ] prototipo con celle colorate su Milano · [ ] dimensione dei tasselli e costo stimato · [ ] D-010 confermata o cambiata

### T-006 — Scaffold del repository per l'iterazione 1
backend-engineer | Backlog | media | S | T-026
Criteri: [ ] tutto eseguibile in locale, senza servizi a pagamento (D-014) · [ ] cartelle `backend/`, `model/`, `app/`, `tests/` · [ ] contratto OpenAPI iniziale · [ ] test eseguiti da `make check`

## Backlog — modello e dati

### T-010 — Metriche di calibrazione e N minimo
data-scientist | Backlog | alta | M | —
Criteri: [ ] definizioni operative in `docs/09-modello.md` §6 · [ ] N minimo per dichiarare una metrica · [ ] metodo di test con dati sintetici etichettati

### T-022 — Risoluzione della griglia H3 (9 o 10)
data-scientist | Backlog | media | S | T-006
Criteri: [ ] confronto su numero di celle, eventi attesi per cella, effetto sulla soglia k · [ ] decisione in `docs/05-decisioni.md`

### T-024 — Licenze e standard per fornire il dato a terzi
privacy-compliance | Backlog | media | M | —
Criteri: [ ] vincoli ODbL sui dati derivati da OSM, con fonte ufficiale · [ ] standard di scambio dei dati di sosta esistenti · [ ] regole per tenere separata l'origine dei dati · [ ] esito in `docs/06-dati.md`

### T-025 — Strade verso le app di mappe e mercato del dato di sosta
competitor-analyst | Backlog | bassa | M | T-004
Criteri: [ ] chi fornisce oggi dati di sosta a mappe e case auto, e come · [ ] programmi per partner di Google, Apple, Waze · [ ] cosa chiedono (copertura, prove di qualità) · [ ] sezione in `docs/02-concorrenza.md` · [ ] nessun contatto esterno

### T-026 — Schema "città come configurazione" e adattatori
backend-engineer | In corso (avviato: `cities/milano`, `parking_core`, test) | alta | M | —
Criteri: [ ] schema del file di città e dell'interfaccia degli adattatori · [ ] `cities/milano` come primo caso · [ ] test che fallisce se il nucleo contiene valori di Milano · [ ] con `data-scientist`: variabili del modello definite in modo indipendente dalla città

### T-023 — Modello a tassi con concorrenza e penetrazione (ricerca)
data-scientist | Backlog | bassa | L | T-010
Criteri: [ ] formulazione scritta · [ ] condizioni per adottarlo rispetto al Beta-Binomiale

## Backlog — UX e marketing

### T-009 — Flussi e schermate
ux-designer | Backlog | media | M | T-004
Criteri: [ ] onboarding con consenso, mappa, contributi, diritti in 3 tap · [ ] zone leggibili senza colore · [ ] `docs/08-ux.md` completato

### T-008 — Posizionamento e ASO (IT + EN)
marketing-sales | Backlog | media | M | T-004
Criteri: [ ] messaggio chiave e tre titoli IT/EN · [ ] parole chiave e screenshot · [ ] solo bozze in `docs/11-marketing.md`

## In corso

_Nessun task._
