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
- **Stato:** approvata dal fondatore il 2026-11-14 per lo sviluppo; **hosting rinviato al lancio** (D-014)
- **Scelta:** app **Flutter**; backend **Python + FastAPI** con contratto OpenAPI come fonte unica; modello in Python (pandas, NumPy, SciPy, statsmodels; PyMC solo se serve); **PostgreSQL + PostGIS**, griglia **H3**; hosting UE.
- **Hosting raccomandato:** un server virtuale in UE (es. Hetzner) con tutto in Docker, più archivio statico con CDN (es. Cloudflare R2) per griglia e tasselli. Stima **5–15 €/mese fino a 10.000 utenti** **[verificare]**: prezzi presi da fonti secondarie, da rileggere sulle pagine ufficiali prima di attivare (→ `fonti.md`).
- **Alternative:** Postgres gestito (Neon, Supabase): gratuito all'inizio ma a consumo e con PostGIS e regione UE da verificare. Fly.io: prezzi non verificati. React Native: nessun vantaggio strutturale su mappe e localizzazione.
- **Conseguenze:** backup e manutenzione del server a nostro carico; nessuna fattura a consumo.

## D-004 — Nessun dato Google nel modello
- **Data:** 2026-11-14 (aggiornata dopo T-002)
- **Stato:** approvata; testo ufficiale corrente letto il 2026-11-14 (sez. 3.2.3: divieto di estrazione, cache, contenuti derivati e uso con mappe non Google). I link a Google Maps non richiedono chiave API. Mostrare i nostri dati sopra una mappa Google è ammesso secondo la nostra lettura, da confermare da un legale prima del lancio
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
- **Stato:** approvata dal fondatore il 2026-11-14 per lo sviluppo e la beta. **Google Maps è previsto in seguito**: il fondatore lo vuole nel prodotto sul mercato. La mappa sta quindi dietro un'interfaccia unica, così il motore si cambia senza toccare il resto. Costi e termini di Google si valutano prima del lancio (T-002)
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

## D-013 — Scalabilità: altre città, altri paesi, integrazione nelle app di mappe
- **Data:** 2026-11-14
- **Stato:** approvata dal fondatore come visione; ogni espansione resta una decisione separata
- **Contesto:** l'obiettivo finale è portare la stima in altre città italiane, poi all'estero, e idealmente dentro app come Google Maps, Apple Mappe o Waze.
- **Scelta — regole di costruzione valide da subito:**
  1. **Città come configurazione.** Un file per città: confine, fuso orario, lingue, valuta, fonti dati, regole di sosta, parametri del modello. Nessun valore di Milano nel codice.
  2. **Fonti e regole come adattatori.** Il nucleo conosce solo uno schema comune (cella, fascia, tipo di sosta, regola). Ogni fonte locale ha il suo adattatore.
  3. **Basi globali dove esistono:** griglia H3 e OpenStreetMap coprono il mondo; le fonti comunali sono un arricchimento, non un requisito.
  4. **Modello trasferibile.** Variabili definite in modo uguale ovunque; una città nuova parte da un prior appreso dalle città già calibrate, con affidabilità bassa dichiarata.
  5. **Lingue senza limiti:** testi in file di traduzione, formati di data, ora, valuta e unità dal sistema; nessuna assunzione su due sole lingue.
  6. **API come prodotto.** Contratto OpenAPI versionato, pensato anche per un cliente esterno: stima, affidabilità, età del dato, versione del modello.
  7. **Prove di qualità pubblicabili.** Calibrazione misurata per città e per periodo, riproducibile: è ciò che un partner chiederà per primo.
  8. **Dati con origine separata e documentata.** Eventi nostri, dati OSM e open data restano distinguibili, con licenza per ciascuno: serve per concedere il dato in licenza.
  9. **Privacy che regge una verifica esterna:** nessun dato personale negli aggregati forniti a terzi; soglia k applicata anche all'API.
- **Cosa NON facciamo ora:** nessuna infrastruttura multi-regione, nessun dato di altre città, nessuna traduzione oltre IT/EN, nessun contatto con partner. Costruire per scalare non significa costruire in grande.
- **Da verificare (T-024, T-025):** vincoli della licenza ODbL sulla cessione di dati derivati da OSM; standard di scambio dei dati di sosta; programmi per partner delle app di mappe; norme sulla posizione fuori dall'UE.

## D-014 — Nessuna spesa fino a quando il prodotto è pronto per il mercato
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** fino al lancio pubblico non si attiva nessun servizio a pagamento. Sviluppo, modello e pagina interna girano in locale (Docker) e sulla CI gratuita.
- **Conseguenze:**
  - Iterazione 1: nessun impatto, è tutta in locale.
  - Iterazione 2 (beta): serve un server raggiungibile dai tester. Solo piani gratuiti, da verificare; creare l'account resta un'azione del fondatore.
  - TestFlight richiede l'account Apple a pagamento: la beta parte da Android con installazione diretta, salvo eccezione (decisione 1 in `TASKS.md`).
  - Prima del lancio si presenta al fondatore il conto completo: account store, hosting, mappa.

## D-015 — Nessuna rilevazione sul campo del fondatore
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** il fondatore non può fare rilevazioni in strada. I primi dati reali sono gli esiti dei tester della beta.
- **Conseguenze:** fino alla beta il prior **non è validato** e va mostrato sempre con affidabilità bassa. La validazione usa una quota di esiti dei tester tenuta da parte e "missioni" di copertura (T-021). Il criterio di abbandono sul prior si sposta dall'iterazione 1 alla 2.

## D-016 — Beta su dati reali e in tempo reale
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore (obiettivo); modalità proposte, soggette al parere di `privacy-compliance`
- **Contesto:** il fondatore vuole una beta basata su dati veri e attuali, non su stime storiche. Verifica T-027: per Milano **non esiste alcuna fonte pubblica in tempo reale sull'occupazione della sosta su strada** (nessun sensore, nessun feed dei parcheggi ATM). L'unica misura reale sono i contributi degli utenti.
- **Scelta — tutte le vie per avere dati reali, in ordine:**
  1. **Tap manuale** con esito ("trovato subito / dopo un po' / non trovato"). Ammesso in beta con consenso.
  2. **"Ricorda dove ho parcheggiato"**: salvare e riprendere l'auto genera gli eventi di sosta e di partenza.
  3. **Rilevamento automatico via Bluetooth dell'auto** (la disconnessione segnala la sosta, la riconnessione la partenza). Tutto sul dispositivo, l'utente sceglie l'auto, zone escluse (casa, lavoro). **Solo dopo DPIA** (T-028).
  4. **Missioni per i tester**: zone e orari da coprire, scelti da noi.
  5. **Contesto in tempo reale** come variabili: meteo, scioperi, eventi, stazioni BikeMi; traffico TomTom solo se i termini lo permettono (T-031).
  6. **Pubblicazione frequente** della griglia: ogni 5 minuti (D-019), con età della stima sempre visibile.
- **Rilevamento tramite posizione:** vedi D-018.
- **Escluso:** dati Google (D-004); Waze (richiede un accordo, decisione del fondatore).
- **Limite da risolvere (T-029):** con 10–20 tester la soglia di k = 5 contributori per cella e fascia non si raggiunge quasi mai, e i dati reali resterebbero invisibili. Proposte da valutare: beta concentrata in poche zone del centro, celle più grandi e fasce più larghe durante la beta.

## D-017 — Beta solo Android, a costo zero
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** la beta parte solo su Android, con installazione diretta del file dell'app. Dettagli e rischi in `10-release.md`.
- **Conseguenze:** nessun account a pagamento. L'account Android gratuito a distribuzione limitata (fino a 20 dispositivi) serve solo dal 2027 e lo crea il fondatore. iPhone, TestFlight e Google Play (25 USD, 12 tester per 14 giorni) si rinviano al lancio. Server della beta: solo piani gratuiti, da verificare sulle pagine ufficiali (T-030).

## D-018 — L'app impara da sola: rilevamento automatico tramite posizione
- **Data:** 2026-11-14
- **Stato:** **voluta dal fondatore; veto di `privacy-compliance` su questa forma (2026-11-14)**. Approvata solo con le condizioni C1–C12 di `15-dpia-bozza.md`, per la beta chiusa: attende la decisione del fondatore e poi la firma della DPIA. Il parere preliminare di `privacy-compliance` era contrario per la prima beta: la DPIA deve mostrare che le condizioni qui sotto bastano.
- **Scelta:** con il consenso dell'utente, il telefono capisce da solo quando il conducente sta cercando posto, quando ha parcheggiato, quanto ci ha messo e quando riparte.
- **Perché conta:** il tempo di ricerca misurato è esattamente il bersaglio del modello ("posto trovato entro 5 minuti"). È il dato migliore che possiamo avere, e arriva senza chiedere nulla all'utente.
- **Condizioni di progetto (non negoziabili):**
  1. Tutto il calcolo avviene sul telefono. Il percorso non lascia mai il dispositivo e viene cancellato appena prodotto l'evento.
  2. Al server arriva solo: tipo di evento, cella, fascia oraria, **tempo di ricerca a scaglioni** (0–2, 2–5, 5–10, oltre 10 minuti), identificatore a rotazione.
  3. Consenso separato ed esplicito; funzione spenta in partenza; interruttore sempre visibile; l'app funziona anche senza.
  4. Zone escluse scelte dall'utente (casa, lavoro), applicate sul telefono.
  5. Conferma facoltativa con un tap ("Hai parcheggiato in strada?") per scartare garage e cortili: le risposte migliorano il rilevamento.
  6. Consumo di batteria misurato in beta, con soglia massima da fissare.
- **Come l'app si migliora da sola:** ogni esito aggiorna la stima al ciclo successivo; emivita, peso dei dati recenti e soglie si ricalibrano periodicamente su dati reali tenuti da parte; un peggioramento della calibrazione apre un task automatico (T-032).
- **Vincoli esterni:** per la beta con installazione diretta non serve l'approvazione di Google. Per Google Play la posizione in background richiede dichiarazione e approvazione: va dimostrato che è essenziale alla funzione principale (`10-release.md`).

## D-020 — Agente dedicato alla grafica e valutazione periodica degli agenti
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** nuovo agente `visual-designer` (solo grafica, sotto `ux-designer`). Gli agenti si valutano a ogni chiusura di iterazione in `14-valutazione-agenti.md`; le correzioni entrano nelle loro definizioni ("Lezioni apprese"). `privacy-compliance` e `competitor-analyst` ricevono Bash, limitato allo script di lettura delle fonti.

## D-019 — Aggiornamento ogni 5 minuti
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** la griglia si ricalcola e si pubblica ogni 5 minuti. Gli esiti degli ultimi 45 minuti pesano di più e valgono per "adesso" qualunque sia la fascia (parametri in `cities/<città>/city.yaml`, da validare).
- **Conseguenze:** l'app riscarica un file piccolo ogni 5 minuti mentre è aperta. La pubblicazione resta a intervalli fissi, come richiesto dalla privacy: `privacy-compliance` verifica in T-018 che 5 minuti con soglia k non permettano di isolare un contributo.
