# 15 — DPIA (bozza)

**BOZZA — non firmata, richiede revisione di un professionista e firma del fondatore.**

Redatta da `privacy-compliance` il 2026-11-14 (T-018, T-028). Secondo la nostra lettura; non è un parere legale. Ogni riferimento marcato **[verificare]** non è stato letto alla fonte ufficiale: i siti eur-lex.europa.eu, edpb.europa.eu e garanteprivacy.it non sono raggiungibili dalla rete di lavoro (da abilitare). Fonti → [`fonti.md`](fonti.md). Decisioni di partenza: D-016, D-018, D-019 in [`05-decisioni.md`](05-decisioni.md). Vincoli sintetici → [`03-privacy.md`](03-privacy.md#vincoli-tecnici-v2).

## 1. Perché una DPIA

- Il fondatore l'ha resa condizione di D-018. Indipendentemente da questo, secondo la nostra lettura il rilevamento automatico soddisfa almeno due criteri delle linee guida WP29/EDPB sulla DPIA (WP248 rev.01) **[verificare]**: dati di localizzazione raccolti in modo sistematico e uso innovativo di tecnologie (posizione in background + Bluetooth).
- Art. 35 GDPR, par. 1 e 7 (contenuto minimo) **[verificare]**; elenco del Garante dei trattamenti soggetti a DPIA (provv. n. 467 dell'11/10/2018) **[verificare]** se includa la geolocalizzazione.
- Ambito: **beta chiusa Android**, 10–20 tester, installazione diretta (D-017). Il lancio pubblico e Google Play richiedono una nuova revisione di questa DPIA.

## 2. Titolare, soggetti, contesto

- Titolare: il fondatore (persona fisica). Nessun DPO nominato (verificare l'obbligo con un professionista al lancio) **[verificare]**.
- Interessati: tester adulti, reclutati direttamente, spesso **conoscenti tra loro e del fondatore**. Questo aumenta il rischio di re-identificazione per conoscenza di contesto.
- Sub-responsabili: hosting gratuito in UE da scegliere (T-030). Nessun SDK di terze parti per analytics o pubblicità.
- Area: Comune di Milano, griglia H3 (ris. 9 proposta, `cities/milano/city.yaml`), fasce di 30 minuti, finestra "adesso" di 45 minuti, emivita 21 giorni, k = 5.

## 3. Descrizione dei trattamenti

| # | Trattamento | Dati sul telefono | Dati al server | Conservazione server |
|---|---|---|---|---|
| T1 | Tap manuale con esito | Cella, fascia, esito | Tipo, cella, fascia, esito, pseudonimo | 30 giorni grezzi, poi solo aggregati |
| T2 | "Ricorda dove ho parcheggiato" | Coordinate dell'auto, ora | **Nulla** (se l'utente acconsente a T1, il salvataggio può generare un evento T1) | — |
| T3 | Rilevamento automatico (posizione in background + Bluetooth dell'auto) | Percorso temporaneo, auto Bluetooth scelta, zone escluse | Tipo (sosta / ripartenza), cella, fascia, tempo di ricerca a scaglioni (0–2, 2–5, 5–10, >10 min), pseudonimo | 30 giorni grezzi, poi solo aggregati |
| P | Pubblicazione della griglia ogni 5 minuti | Download del file intero | — | File statico pubblico/beta |

Flusso T3: Bluetooth disconnesso dall'auto scelta → telefono stima l'inizio della ricerca dal percorso recente → sosta → calcolo del tempo di ricerca → riduzione a cella + fascia + scaglione → cancellazione del percorso → invio. Riconnessione → evento di ripartenza (cella, fascia).

## 4. Finalità e base giuridica

- Finalità unica: stimare la probabilità di trovare posto in strada per cella e fascia. Nessuna profilazione, nessun uso commerciale dei dati individuali, nessun dato Google nel modello (D-004).
- Base: **consenso** (art. 6(1)(a) GDPR **[verificare]**), separato per T1 e T3, revocabile in ogni momento con la stessa facilità con cui è dato (art. 7(3) **[verificare]**).
- Accesso alla posizione e al Bluetooth del terminale: consenso anche ai sensi dell'art. 122 Codice privacy / art. 5(3) direttiva ePrivacy **[verificare]**, oltre ai permessi Android.
- T2 è una funzione per l'utente, solo locale: nessun trattamento lato titolare se nulla lascia il telefono (secondo la nostra lettura).
- Dati di contesto (lingua, versione): interesse legittimo da valutare, fuori da questa DPIA.

## 5. Necessità e proporzionalità

- **Necessità di T3:** il tempo di ricerca è il bersaglio del modello (D-018) e non esiste fonte pubblica in tempo reale (D-016). Il tap manuale non misura il tempo di ricerca in modo affidabile.
- **Alternative meno invasive valutate:**
  - solo Bluetooth senza posizione: dà la sosta ma non la cella → insufficiente;
  - posizione solo in primo piano: perde la sosta, l'utente guida → insufficiente;
  - **riconoscimento dell'attività + Bluetooth come innesco, GPS acceso solo durante la fase di ricerca**: adottata come condizione (C3).
- **Minimizzazione:** l'evento "inizio ricerca" **non** si invia (rivela l'area di destinazione); basta lo scaglione sull'evento di sosta. Durata della sosta non inviata.
- **Proporzionalità della beta:** pochi tester rendono gli aggregati quasi sempre sotto soglia (T-029): il beneficio immediato è limitato, quindi le misure devono rendere il rischio individuale molto basso.

## 6. Rischi

Scala: probabilità e gravità 1 (bassa) – 4 (massima). Valutazione **senza** le correzioni di §7, cioè con D-018 com'è scritta.

| ID | Rischio | Prob. | Grav. | Nota |
|---|---|---|---|---|
| R1 | **Re-identificazione da celle e orari ripetuti.** Con un ID a rotazione 24h il server lega tutte le soste di un giorno: una sequenza di 3–4 punti spazio-temporali basta di norma a identificare una persona (letteratura, fonte secondaria). | 3 | 3 | Rischio principale della configurazione D-018 |
| R2 | **Inferenza casa/lavoro** da soste ricorrenti nella stessa cella e fascia (mattina/sera). Può rivelare anche luoghi sensibili (salute, culto). | 3 | 3 | Zone escluse solo se l'utente le imposta |
| R3 | **Isolamento tra due pubblicazioni a 5 minuti.** Con finestra mobile di 45 minuti, la differenza tra due griglie consecutive rivela il contributo appena entrato: una cella che passa da sotto a sopra soglia, o cambia valore o affidabilità, dice "qualcuno era lì, con questo esito". | 3 | 2 | Intervalli fissi impediscono solo interrogazioni a piacere, **non** il confronto tra versioni |
| R4 | **Pochi tester e soglia k.** Con 24h di rotazione, nella componente storica (21 giorni) una sola persona che parcheggia 5 giorni nella stessa cella vale 5 "contributori": k = 5 è soddisfatta da **una** persona. Tester che si conoscono aggiungono conoscenza di contesto. | 4 | 3 | La soglia k, così contata, non protegge |
| R5 | **ID a rotazione e diritti.** Dopo la rotazione il titolare non può ritrovare i dati: accesso e cancellazione diventano impossibili, ma il dato resta riconducibile da chi ha conoscenza esterna. | 2 | 2 | Art. 11 GDPR **[verificare]** |
| R6 | **Indirizzo IP e ora di arrivo** del pacchetto legano eventi oltre lo pseudonimo, anche presso il fornitore di hosting. | 2 | 3 | Dipende da T-030 |
| R7 | **Backup automatico Android** copia sul cloud Google le coordinate di T2 e le zone escluse. | 2 | 3 | Configurazione dell'app |
| R8 | Percorso sul telefono conservato oltre il necessario o in log di debug. | 2 | 3 | |
| R9 | Consenso non libero (tester amici del fondatore) o non informato sulla posizione in background. | 2 | 2 | |

## 7. Misure (condizioni vincolanti)

Le condizioni C1–C12 sono riportate in sintesi in [`03-privacy.md`](03-privacy.md#vincoli-tecnici-v2).

- **C1 — Pseudonimo per cella al posto dell'ID 24h (R1, R4, R5).** Ogni evento porta `pid = HMAC(segreto_dispositivo, tipo ‖ cella ‖ epoca_28gg)`. Il server **non può collegare** eventi di celle diverse né la sosta alla ripartenza; può contare contributori distinti per cella su tutta la finestra storica. Il segreto non lascia mai il telefono.
- **C2 — k contata correttamente (R4).** k = 5 pseudonimi distinti per cella, fascia e tipo, sia nella finestra "adesso" sia nella componente storica. **k non si abbassa in beta**: per avere celle visibili si allargano celle e fasce (T-029), non si riduce la soglia.
- **C3 — Rilevamento sobrio (necessità).** Innesco: Bluetooth dell'auto scelta + riconoscimento attività "in auto". GPS acceso solo durante guida a bassa velocità prima della sosta, con durata massima (es. 20 min). Servizio in primo piano con notifica visibile mentre è attivo.
- **C4 — Percorso effimero (R8).** Solo in memoria, mai su disco né nei log; cancellato alla produzione dell'evento o dopo il timeout. Nome e indirizzo Bluetooth dell'auto restano sul telefono.
- **C5 — Eventi minimi.** Al server solo sosta (con scaglione) e ripartenza. Niente "inizio ricerca", niente durata della sosta, niente coordinate, niente ora esatta.
- **C6 — Anti-differenza (R3).** Una cella viene aggiornata nella griglia solo se, dall'ultimo valore pubblicato, ci sono **almeno 2 nuovi pseudonimi distinti**; altrimenti resta il valore precedente. Il file pubblica la probabilità in **classi** (max 4) e l'affidabilità in **3 livelli** con soglie ben sopra k; **mai conteggi**.
- **C7 — Invio ritardato e senza tempo di arrivo (R3, R6).** Il telefono invia con ritardo casuale 0–10 min; il server scarta l'ora di arrivo e conserva solo la fascia. Nessun IP nei log applicativi e nella configurazione del fornitore (vincolo per T-030).
- **C8 — Zone escluse proposte in automatico (R2).** Al primo avvio di T3 l'app propone come zone escluse le celle dove il telefono resta di notte e nelle ore di lavoro (calcolo locale). Raggio minimo: la cella H3 e le sue vicine. Nessun evento parte da una zona esclusa.
- **C9 — Limite di frequenza sul telefono (R2).** Al massimo 1 evento per tipo e per cella al giorno.
- **C10 — Diritti (R5).** Il telefono tiene il registro locale dei propri contributi (visibile all'utente). Accesso e cancellazione: il telefono ricalcola i `pid` e li invia (art. 11(2) **[verificare]**). Dopo 30 giorni il dato grezzo non esiste più; gli aggregati non contengono pseudonimi. Disinstallare cancella il segreto: va detto nell'informativa.
- **C11 — Niente backup cloud (R7).** `allowBackup=false` / regole di estrazione dati che escludono coordinate, zone escluse, segreto e registro.
- **C12 — Consenso e informativa per i tester (R9).** Consenso T3 separato, spento in partenza, spiegato con una schermata che dice "anche quando l'app è chiusa"; revoca in ≤ 3 tap; nota informativa scritta per i tester che dica che chi li conosce potrebbe dedurre la loro presenza in una zona; partecipare a T3 non è condizione per la beta.
- **Sempre:** test di re-identificazione (§9) verde prima di ogni build distribuita; griglia di beta non indicizzata e distribuita solo ai tester.

## 8. Rischio residuo (con C1–C12)

| ID | Prob. | Grav. | Residuo | Motivo |
|---|---|---|---|---|
| R1 | 1 | 3 | Basso | Nessun collegamento tra celle |
| R2 | 2 | 2 | Medio-basso | Restano ricorrenze nella stessa cella fuori dalle zone escluse, entro 30 giorni |
| R3 | 1 | 2 | Basso | Delta ≥ 2, classi, ritardo casuale |
| R4 | 2 | 2 | Medio-basso | Conoscenza tra tester non eliminabile; mitigata da informativa e k reale |
| R5 | 1 | 2 | Basso | Diritti esercitabili dal telefono |
| R6 | 2 | 2 | Medio-basso | Dipende dal fornitore (T-030) |
| R7–R9 | 1 | 2 | Basso | Configurazione e test |

Nessun rischio residuo alto: secondo la nostra lettura non serve consultazione preventiva del Garante (art. 36 **[verificare]**). Da riconfermare al lancio pubblico.

## 9. Test di re-identificazione (prima di ogni release)

1. Script `scripts/reid_test.py`, target `make reid`, eseguito in CI su ogni build distribuita; esito rosso = release bloccata.
2. Simula 20 agenti con casa, lavoro e abitudini (seme fisso) e genera eventi passando per il **codice reale** del telefono (riduzione, zone escluse, `pid`, ritardo) e del server (aggregazione, pubblicazione ogni 5 min).
3. Attacco A — integrità di k: per ogni cella pubblicata conta gli agenti **veri** distinti; deve essere ≥ k. Un solo caso < k = fallito.
4. Attacco B — differenza: confronta ogni coppia di griglie consecutive; nessun cambiamento deve essere attribuibile a un solo agente.
5. Attacco C — collegamento: dal database grezzo prova a unire eventi di celle diverse (per `pid`, fascia, ordine di arrivo); tasso di ricostruzione di traiettorie > 0 = fallito.
6. Attacco D — casa/lavoro: dal database grezzo stima la cella di casa di ciascun agente; precisione non superiore al caso (+5 punti) = superato.
7. Attacco E — conoscenza esterna: un attaccante conosce un evento di un agente e cerca gli altri suoi eventi; trovarne anche uno = fallito.
8. Scansione di richieste, log e file pubblicati: nessuna coordinata (regex lat/lon), IP, ora esatta, conteggio.
9. Test di contratto: il payload inviato contiene solo i campi di C5; ogni campo in più fa fallire il test.
10. Report in `reports/reid/<data>.json` (solo metriche, nessun dato), allegato alla checklist di release.

## 10. Decisione (proposta di `privacy-compliance`)

| Trattamento | Decisione |
|---|---|
| T1 Tap manuale | **Approvato con condizioni** C1, C2, C5–C7, C10, C12 |
| T2 "Ricorda dove ho parcheggiato" (solo locale) | **Approvato** con C11; se genera eventi, valgono le regole di T1 |
| T3 Rilevamento automatico, nella forma di D-018 (ID 24h, k contata su ID giornalieri) | **Veto** (R1, R4 alti; art. 25 e 35(7)(d) GDPR **[verificare]**) |
| T3 Rilevamento automatico con C1–C12 | **Approvato con condizioni**, solo beta chiusa Android, dopo: decisione scritta del fondatore che recepisca C1–C12 in `05-decisioni.md`, firma di questa DPIA, `make reid` verde |
| P Pubblicazione ogni 5 minuti | **Approvata con condizioni** C2, C6, C7; 5 minuti con k = 5 **da soli non bastano** |

Raccomandazione: revisione di un professionista privacy prima della beta con T3 attivo; obbligatoria prima del lancio pubblico e di Google Play.

## 11. Firme

- Redatto: `privacy-compliance`, 2026-11-14 (bozza).
- Revisione professionale: ______ (data) ______
- Approvazione del titolare (fondatore): ______ (data) ______
