# TASKS.md — Board dei task

Fonte unica di verità. Regole in `CLAUDE.md` §6. Massimo 150 righe: i task `Fatto` passano in `docs/archivio/` a chiusura di iterazione.

Formato: `### T-id — titolo` · riga `Ruolo | Stato | Priorità | Budget (S/M/L) | Dipendenze` · `Criteri:` · `Note:` (facoltativa).
Stati: Backlog · In corso (con nome del proprietario) · Bloccato · Fatto.

## Decisioni richieste al fondatore

1. **Rete della sessione:** abilitare i domini ufficiali non raggiungibili (`dati.comune.milano.it`, `support.google.com`, `developers.google.com`, `cloud.google.com`, `apps.apple.com`, `play.google.com`, `pub.dev`, pagine prezzi dei fornitori). Raccomandazione: sì. Sblocca T-001–T-004.
2. **Stack (D-003):** A) Flutter + FastAPI + PostGIS su un server UE, 5–15 €/mese stimati; B) Postgres gestito a consumo. Raccomandazione: A. Nessuna spesa prima dell'iterazione 1.
3. **Mappa (D-010):** A) MapLibre + OpenStreetMap, dopo la prova T-020; B) Google Maps. Raccomandazione: A.
4. **Rilevazioni sul campo e 5 interviste** (iterazione 1, poche ore, le fai tu): sì o no. Raccomandazione: sì; senza, il modello non si può validare.

## Iterazione 0 — verifiche

### T-001 — Open data del Comune di Milano
data-engineer | Bloccato (rete) | alta | M | —
Criteri: [x] esito su stalli e sensori (non esistono, confidenza media) · [ ] riconferma sul catalogo · [ ] Area B/C, lavaggio strade, mercati, strutture · [x] `docs/06-dati.md` aggiornato

### T-002 — Termini Google Maps Platform e norme
privacy-compliance | Bloccato (rete) | alta | M | —
Criteri: [x] parere prudenziale (D-004) · [ ] testo corrente dei termini, sez. 3.2.3 · [ ] deep link Google/Waze · [ ] DSA su Google Play, testo EAA

### T-003 — Requisiti store
release-manager | Bloccato (rete) | alta | M | —
Criteri: [x] requisiti Apple in `docs/10-release.md` · [ ] pagine Google Play (posizione, Data safety, tester chiusi, costo)

### T-004 — Concorrenti sugli store
competitor-analyst | Bloccato (rete) | alta | M | —
Criteri: [x] `docs/02-concorrenza.md` aggiornato da fonti web · [ ] recensioni sugli store · [ ] Find & Park in app a Milano · [ ] SpotAngels e PuliAMO in Italia

### T-005 — Stack e costi
backend-engineer | Fatto (attende decisione 2) | media | S | —
Note: D-003 aggiornata. Prezzi **[verificare]** sulle pagine ufficiali prima di attivare.

### T-007 — Primo ciclo watchdog
ops-watchdog | Fatto | media | S | —
Note: `docs/07-report-watchdog.md`.

## Backlog — prodotto (le 7 idee)

### T-011 — Regole della zona e avviso lavaggio strade
product-manager | Backlog | alta | M | T-001
Criteri: [ ] requisiti e criteri di accettazione · [ ] fonte dati verificata e data della fonte visibile · [ ] avviso "vale la segnaletica" · [ ] riferimento a `02-concorrenza.md`

### T-012 — "Ricorda dove ho parcheggiato" e timer di scadenza
product-manager | Backlog | alta | M | T-018
Criteri: [ ] tutto sul dispositivo · [ ] salvare l'auto propone l'evento "ho parcheggiato", ripartire "ho lasciato", con consenso · [ ] parere di `privacy-compliance`

### T-013 — "Piano B": zona verde vicina, strutture, interscambio
product-manager | Backlog | bassa | S | T-001
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
Criteri: [ ] pro, contro e vincoli privacy per ciascuna in `docs/11-marketing.md` · [ ] raccomandazione · [ ] decisione lasciata al fondatore, non prima dell'iterazione 3

## Backlog — privacy, sicurezza, tecnica

### T-018 — Parere sui vincoli tecnici v2 e test di re-identificazione
privacy-compliance | Backlog | alta | M | —
Criteri: [ ] ogni vincolo di `docs/03-privacy.md` "Vincoli tecnici (v2)" approvato o corretto · [ ] rotazione dell'identificatore e diritti motivati · [ ] specifica del test di re-identificazione · [ ] indice della DPIA

### T-019 — Modello delle minacce e antiabuso
backend-engineer | Backlog | media | M | T-018
Criteri: [ ] `docs/12-sicurezza.md` completato · [ ] limiti di frequenza e controlli di plausibilità definiti · [ ] attestazione del dispositivo valutata con `privacy-compliance`

### T-020 — Prova tecnica della mappa (MapLibre + PMTiles in Flutter)
mobile-engineer | Backlog | alta | M | decisione 2
Criteri: [ ] maturità del pacchetto verificata · [ ] prototipo con celle colorate su Milano · [ ] dimensione dei tasselli e costo stimato · [ ] D-010 confermata o cambiata

### T-006 — Scaffold del repository per l'iterazione 1
backend-engineer | Backlog | media | S | decisione 2
Criteri: [ ] cartelle `backend/`, `model/`, `app/`, `tests/` · [ ] contratto OpenAPI iniziale · [ ] test eseguiti da `make check`

## Backlog — modello e dati

### T-010 — Metriche di calibrazione e N minimo
data-scientist | Backlog | alta | M | —
Criteri: [ ] definizioni operative in `docs/09-modello.md` §6 · [ ] N minimo per dichiarare una metrica · [ ] metodo di test con dati sintetici etichettati

### T-021 — Protocollo di rilevazione sul campo e traccia interviste
data-scientist | Backlog | alta | S | decisione 4
Criteri: [ ] protocollo di una pagina: zone, orari, cosa annotare, quante ripetizioni · [ ] modulo senza dati personali · [ ] 5 domande per le interviste (con `product-manager`)

### T-022 — Risoluzione della griglia H3 (9 o 10)
data-scientist | Backlog | media | S | T-006
Criteri: [ ] confronto su numero di celle, eventi attesi per cella, effetto sulla soglia k · [ ] decisione in `docs/05-decisioni.md`

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
