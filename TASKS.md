# TASKS.md — Board dei task

Fonte unica di verità. Regole in `CLAUDE.md` §6. Massimo 150 righe: i task `Fatto` passano in `docs/archivio/` a chiusura di iterazione.

Formato: `### T-id — titolo` · riga `Ruolo | Stato | Priorità | Budget (S/M/L) | Dipendenze` · `Criteri:` · `Note:` (facoltativa).
Stati: Backlog · In corso (con nome del proprietario) · Bloccato · Fatto.

## Decisioni richieste al fondatore

Decisa il 2026-11-14: repository privato e sito da un repository separato (D-038).

1. **Quattro azioni tue per mettere online il sito** (`docs/05-decisioni.md` D-038): creare il repository pubblico `sostami`; attivare Pages con "GitHub Actions"; rendere privato `Project`; dare a Claude l'accesso al nuovo repository. Poi dimmelo: copio il sito e verifico l'indirizzo.
2. **Durata della beta:** A) 6 settimane; B) 4. Raccomandazione: A.

## Iterazione 1 — in corso

### T-050 — Rendere credibile il modello di occupazione prima di mostrarlo ai tester
data-scientist | Backlog | alta | M | —
Criteri: [ ] il centro risulta troppo facile (es. Brera "almeno 9 su 10" in pieno giorno) e l'occupazione notturna è solo 0,62: rivedere quota di auto dei residenti in strada, lati parcheggiabili, visitatori · [ ] confronto con almeno una fonte esterna (studi, dati AMAT, rilevazioni pubblicate) · [ ] conteggi a campione di auto in sosta su alcune strade (chi li fa: da decidere con il fondatore) · [ ] calibrazione con le prime segnalazioni reali · [ ] nell'app la stima resta marcata "non verificata" finché questi punti non sono chiusi

### T-048 — Verifica del nome SostaMi
legal-analyst | Backlog | alta | S | —
Criteri: [ ] ricerca nei registri UIBM ed EUIPO (classi per software e servizi di mobilità) · [ ] app con nome uguale o simile su Google Play e App Store · [ ] domini liberi · [ ] esito con rischio e alternative; nessuna registrazione, che spetta al fondatore

### T-047 — Verifica indipendente delle correzioni privacy
privacy-redteam | Backlog | alta | M | —
Criteri: [ ] i test adattati da `privacy-engineer` non sono stati indeboliti · [ ] attacchi ripetuti sul codice corretto, più D ed E della DPIA · [ ] attacco al residuo "già ammessi entrano subito nel live" · [ ] esito a `privacy-compliance`, che conferma o no lo stop alla raccolta delle ripartenze

### T-045 — Stima a livelli su tutto il Comune (D-029)
data-scientist | Backlog | alta | L | T-040
Criteri: [ ] livelli: zona, quartiere, settore, città; ogni strada usa il più fine che raggiunge k · [ ] quanta mappa mostra dati reali, per livello, con 20, 100, 300, 1.000 tester · [ ] progetto con `privacy-engineer` contro la sottrazione tra livelli · [ ] attacco del red team superato · [ ] parere di `privacy-compliance` · [ ] il livello è dichiarato nella scheda della strada

### T-041 — Posti per strada: sosta lungo il marciapiede, colori delle strisce, moto (D-030)
data-engineer | In corso | alta | L | —
Criteri: [x] aree di sosta mappate e stima dei posti (`scripts/build_parking.py`) · [x] 74 parcheggi in struttura con posti (D-031) · [ ] tariffe e orari delle strutture · [ ] ripiego: immagini aeree con licenza aperta · [ ] sosta lungo il marciapiede per tratto e per lato · [ ] confronto con una fonte ufficiale · [ ] OpenStreetMap se la rete lo consente · [ ] tariffe e orari per ambito da fonte ufficiale · [ ] stalli moto · [ ] griglia limitata alle celle con strade e al confine comunale

### T-042 — Testo del GDPR e norme non raggiungibili
legal-analyst | Bloccato (EUR-Lex e Garante restituiscono pagine vuote) | media | S | —
Criteri: [ ] articoli 4, 6, 7, 11, 25, 35, 36 e considerando 26 letti alla fonte · [ ] art. 122 Codice privacy · [ ] Linee guida EDPB 1/2020

### T-043 — App Android: ambiente e scheletro
mobile-engineer | Backlog | alta | L | T-040
Criteri: [ ] Flutter e Android SDK installabili nell'ambiente (siti da abilitare elencati) · [ ] scheletro con mappa delle strade, vista live e altri orari, veicolo, contributi · [ ] contratto API dal backend · [ ] testi IT/EN · [ ] requisito: invio con ritardo casuale (C7)

### T-044 — Versione web collegata al servizio (D-035)
backend-engineer | Backlog | alta | M | T-047
Criteri: [ ] la web app legge la griglia pubblicata e invia le segnalazioni con consenso, pseudonimo per cella e ritardo casuale · [ ] GPS con consenso, ridotto a cella sul dispositivo · [ ] versione installabile sulla schermata Home · [ ] mappa di sfondo: dati del Comune o tasselli con licenza adatta · [ ] comando unico per avviare tutto in locale

### T-036 — Veicolo: taglie, moto, elenco modelli (D-023)
data-scientist | Backlog | alta | M | T-034
Criteri: [ ] parere di `privacy-compliance` sull'invio della taglia · [ ] effetto della taglia stimato a livello di città, sostituendo i valori provvisori · [ ] fonte degli stalli moto e regole per le moto a Milano · [ ] fonte con licenza adatta per modelli e lunghezze · [ ] stima per le moto dichiarata indicativa finché manca il modello dedicato

### T-032 — Rilevamento sul dispositivo e miglioramento automatico
data-scientist | Backlog | alta | L | T-034
Criteri: [ ] regole per riconoscere inizio ricerca, sosta e partenza (con `mobile-engineer`) · [ ] scaglioni del tempo di ricerca · [ ] ricalibrazione periodica automatica dei parametri su dati reali riservati · [ ] allarme automatico se la calibrazione peggiora · [ ] misura dei falsi parcheggi e della batteria in beta

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
product-manager | Backlog | alta | M | —
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

### T-019 — Modello delle minacce e antiabuso
backend-engineer | Backlog | media | M | —
Criteri: [ ] `docs/12-sicurezza.md` completato · [ ] limiti di frequenza e controlli di plausibilità definiti · [ ] attestazione del dispositivo valutata con `privacy-compliance`

### T-020 — Prova tecnica della mappa (MapLibre + PMTiles in Flutter)
mobile-engineer | Backlog | alta | M | —
Criteri: [ ] mappa dietro un'interfaccia unica, sostituibile con Google Maps (D-010) · [ ] maturità del pacchetto verificata · [ ] prototipo con celle colorate su Milano · [ ] dimensione dei tasselli e costo stimato · [ ] D-010 confermata o cambiata

## Backlog — modello e dati

### T-024 — Licenze e standard per fornire il dato a terzi
privacy-compliance | Backlog | media | M | —
Criteri: [ ] vincoli ODbL sui dati derivati da OSM, con fonte ufficiale · [ ] standard di scambio dei dati di sosta esistenti · [ ] regole per tenere separata l'origine dei dati · [ ] esito in `docs/06-dati.md`

### T-025 — Strade verso le app di mappe e mercato del dato di sosta
competitor-analyst | Backlog | bassa | M | T-004
Criteri: [ ] chi fornisce oggi dati di sosta a mappe e case auto, e come · [ ] programmi per partner di Google, Apple, Waze · [ ] cosa chiedono (copertura, prove di qualità) · [ ] sezione in `docs/02-concorrenza.md` · [ ] nessun contatto esterno

### T-023 — Modello a tassi con concorrenza e penetrazione (ricerca)
data-scientist | Backlog | bassa | L | T-010
Criteri: [ ] formulazione scritta · [ ] condizioni per adottarlo rispetto al Beta-Binomiale

## Backlog — UX e marketing

### T-033 — Sistema visivo e schermate mancanti
visual-designer | Backlog | media | M | T-009
Criteri: [ ] direzione approvata (D-024): mantenerla · [ ] mappa reale con strade colorate · [ ] modalità scura · [ ] privacy e diritti, onboarding completo, stato senza rete · [ ] stile della mappa reale (con T-020) · [ ] token pronti per `mobile-engineer`

### T-009 — Flussi e schermate
ux-designer | Backlog | media | M | T-004
Criteri: [ ] onboarding con consenso, mappa, contributi, diritti in 3 tap · [ ] zone leggibili senza colore · [ ] `docs/08-ux.md` completato

## In corso

_Nessun task._
