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
- **Stato:** approvata **con le condizioni C1–C12** di `15-dpia-bozza.md`, accettate dal fondatore il 2026-11-14, per la sola beta chiusa. Si attiva dopo revisione professionale e firma della DPIA. Le condizioni di progetto qui sotto valgono dove C1–C12 non dicono altro. Il parere preliminare di `privacy-compliance` era contrario per la prima beta: la DPIA deve mostrare che le condizioni qui sotto bastano.
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

## D-021 — Mappa a livello di strada
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** l'utente vede la disponibilità **sulla singola strada**, colorata con gli stessi livelli (colore più tratto), sopra una mappa stradale normale. Le zone esagonali non si mostrano più.
- **Come si concilia con la privacy:** il calcolo e i contributi restano per cella (condizioni C1, C2). Ogni tratto di strada prende la stima della sua cella, corretta dalle caratteristiche fisse del tratto (numero e tipo di stalli, regole di sosta, da OSM e open data).
- **Limite da dichiarare:** due strade della stessa cella differiscono solo per le caratteristiche fisse, non per dati live propri. Inviare al server il tratto di strada invece della cella sarebbe una nuova raccolta: serve un parere di `privacy-compliance` (T-035).
- **Conseguenze:** serve la rete stradale da OSM con gli attributi di sosta (T-035); la griglia pubblicata resta per cella, la geometria delle strade è un file statico a parte.

## D-022 — Vista sempre live, con altri orari e giorni come stime
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** la mappa si apre sempre sulla situazione di adesso. L'utente può scegliere un altro orario o giorno della settimana: in quel caso vede una **stima**, indicata come tale, senza la componente "adesso".
- **Conseguenze:** si pubblicano due file: la griglia live (ogni 5 minuti) e la tabella delle stime per fascia e tipo di giorno (ricalcolata una volta al giorno).

## D-023 — Taglia del veicolo e moto
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore (cambio di scope: le moto entrano nel prodotto)
- **Scelta:** l'utente indica il veicolo (ricerca per modello oppure taglia: moto o scooter, auto piccola, media, grande o furgone). La stima si adatta: più piccolo è il veicolo, più è facile trovare posto.
- **Privacy:** il modello resta sul telefono; la correzione per taglia si applica sul telefono, quindi per vedere la mappa non si invia nulla. Con i contributi viaggerebbe solo la taglia (4 valori): è un dato in più e serve il parere di `privacy-compliance` (T-036). L'effetto della taglia si stima a livello di città, non per cella, così la soglia k non si frammenta.
- **Onestà sui numeri:** i moltiplicatori iniziali sono ipotesi non validate (in `cities/<città>/city.yaml`); vanno sostituiti da valori appresi sugli esiti reali.
- **Moto:** hanno stalli e regole propri. Serve una fonte per gli stalli moto e un modello dedicato (T-036); fino ad allora la stima per le moto è indicativa.
- **Elenco dei modelli:** serve una fonte con licenza adatta per modello e lunghezza; fino ad allora si sceglie la taglia.

## D-024 — Direzione grafica approvata
- **Data:** 2026-11-14
- **Stato:** approvata dal fondatore
- **Scelta:** la direzione della prima bozza (chiara e sobria, token in `16-grafica.md`) è confermata e vale per tutto il lavoro grafico futuro.

## D-025 — Team privacy
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** `privacy-compliance` guida tre specialisti: `privacy-engineer` (meccanismi tecnici e test), `privacy-redteam` (attacca le nostre protezioni), `legal-analyst` (fonti primarie, licenze, bozze). Il veto resta di `privacy-compliance`.
- **Motivo:** la valutazione del ciclo 1 ha mostrato due limiti del ruolo unico: norme non lette alla fonte e nessuno che provasse davvero a rompere le protezioni.
- **Costo:** tre descrizioni in più caricate a ogni sessione; si delega solo la parte che serve.

## D-026 — Linee sottili e continue sulla mappa
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** le strade sono colorate con linee continue e sottili, senza coprire la strada. Niente tratteggi.
- **Accessibilità:** senza il tratto, la distinzione tra livelli si affida a colore e luminosità. Per non affidarsi al solo colore: livello sempre scritto nella scheda della strada, e modalità "alta leggibilità" nelle impostazioni che riattiva tratti diversi (T-033).

## D-027 — Strade dal Database Topografico del Comune
- **Data:** 2026-11-14
- **Stato:** approvata (scelta tecnica, reversibile)
- **Contesto:** i siti di OpenStreetMap risultano abilitati ma la connessione dalla sessione viene interrotta. Nel catalogo del Comune esiste il Database Topografico 2020 (licenza CC BY), con tutti gli elementi stradali e i loro nomi.
- **Scelta:** la rete stradale di Milano viene dal Database Topografico (strato `EL_STR`), tramite l'adattatore `cities/milano/adapter.py`. OpenStreetMap resta come fonte di riserva e per le altre città.
- **Vantaggi:** fonte ufficiale; la licenza CC BY chiede solo l'attribuzione e non ha il vincolo "condividi allo stesso modo" di OpenStreetMap, che pesava sulla cessione del dato a terzi (R-16).
- **Limiti:** dati del 2020; nessun attributo di sosta sui tratti (stalli, strisce, moto): vanno da altre fonti; escluse pertinenze private e tangenziali.
- **Risultato:** 24.008 elementi stradali, 30.727 tratti collegati a 1.654 celle, tutti con nome.

## D-028 — Lavoro autonomo del team
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** il team lavora anche senza richiesta, con la sessione principale come CEO. Un'attività programmata esegue un ciclo ogni giorno alle 03:41 (ora italiana) in questa stessa sessione. Procedura, limiti di costo e definizione di "beta valida" in `17-autonomia.md`.
- **Limiti invariati:** le decisioni di `CLAUDE.md` §7 restano del fondatore. In particolare **gli agenti non creano account**: un account lega legalmente una persona e richiede la sua email e la sua identità. Quando serve, il ciclo prepara tutto e indica il singolo passo da fare.

## D-029 — La beta copre tutto il Comune di Milano
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore (tassativa). La proposta di una beta concentrata in un quartiere è respinta.
- **Conseguenza da gestire:** con la soglia di 5 contributori (mai abbassata) e zone piccole, su tutta la città i dati reali non raggiungono quasi mai la soglia (`09-modello.md` §10).
- **Soluzione proposta — stima a livelli (T-045), soggetta al parere di `privacy-compliance`:** ogni strada mostra il dato reale del livello più fine che raggiunge la soglia: zona di qualche isolato → quartiere → settore della città → intera città. Il livello "intera città" si raggiunge presto anche con pochi tester, quindi tutta la mappa riflette dati reali fin dall'inizio; il dettaglio cresce dove arrivano più contributi. Le differenze tra strade vicine vengono dalle caratteristiche fisse dei tratti.
- **Onestà:** la scheda di ogni strada dice a quale livello si riferisce il dato ("questa zona", "questo quartiere", "tutta Milano").
- **Rischio privacy nuovo:** pubblicare più livelli insieme permette di sottrarre un livello dall'altro. Va progettato e attaccato dal red team prima di essere attivato.
- **Leva principale:** più tester. Fino al 2027 l'installazione diretta su Android non ha il limite di 20 dispositivi: il numero di tester dipende solo dal reclutamento, che spetta al fondatore.
- **Missioni:** restano, per indirizzare i tester dove mancano dati, ma senza limitare l'area.

## D-030 — Dove sono i parcheggi e quanti posti hanno
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore (obiettivo); primo passo fatto
- **Scelta:** l'app deve sapere dove sono i posti e quanti sono, strada per strada, e usarlo per essere più precisa.
- **Fatto:** dal Database Topografico del Comune (strato `AC_VEI`, aree "PARCHEGGIO") sono state estratte **3.090 aree di sosta mappate**; dalla loro forma si stimano circa **123.000 posti** (circa 102.000 in aree grandi, 19.000 in fasce a pettine o a spina, 3.000 in fasce in linea), assegnati a 1.758 tratti di strada in 826 celle. Comandi: `scripts/build_parking.py`. Regole di stima in `parking_core/capacity.py`.
- **Limiti da dichiarare:** è una stima dalla geometria, non un conteggio di stalli; dati del 2020; le aree grandi possono includere parcheggi privati o di strutture; **i posti lungo il marciapiede dipinti sulla carreggiata non sono in questo strato**, e a Milano sono la maggior parte della sosta su strada. Il numero non è confrontato con una fonte ufficiale.
- **Prossimi passi (T-041):** censire la sosta lungo il marciapiede (lunghezza dei tratti per lato, corretta da passi carrai, incroci e divieti; OpenStreetMap se raggiungibile; contributi degli utenti), distinguere strisce blu, bianche, gialle e stalli moto, usare i posti per tratto come variabile del modello e validarla sugli esiti reali.

## D-031 — Parcheggi in struttura sulla mappa; immagini aeree come ripiego
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** oltre alla sosta su strada, la mappa mostra i parcheggi al coperto e a pagamento (autorimesse, parcheggi pubblici, interscambio).
- **Fatto:** 74 strutture con nome, indirizzo e posti (circa 29.000 posti) dai dataset del Comune ds342 e ds45 (CC BY), nell'adattatore di Milano e nella pagina di anteprima.
- **Mancano:** tariffe, orari, posti liberi in tempo reale (nessuna fonte pubblica trovata); autorimesse private non convenzionate.
- **Ripiego per la sosta lungo il marciapiede:** se né il Database Topografico né OpenStreetMap bastano, si usano immagini aeree con licenza aperta (ortofoto pubbliche, fonte e licenza da verificare) per riconoscere le file di auto in sosta. Le immagini satellitari di Google non si possono usare: i loro termini vietano di ricavarne contenuti (D-004). Costo: alto (scarico e riconoscimento delle immagini); si tenta solo dopo le altre vie (T-041).

## D-032 — Ciclo autonomo alleggerito e in una chat separata
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore (il ciclo giornaliero consumava troppo e riempiva la chat principale)
- **Scelta:** il ciclo gira in una sessione dedicata ("App parcheggi - cicli autonomi"), il martedì e il venerdì alle 03:41, con al massimo 2 deleghe. La chat principale resta per le decisioni. Sostituisce la cadenza indicata in D-028.

## D-033 — Nome "SostaMi" e logo
- **Data:** 2026-11-14
- **Stato:** nome scelto dal fondatore; **marchio non ancora verificato** (registri UIBM ed EUIPO, nomi già presenti sugli store): la verifica va fatta prima di usarlo in pubblico (T-048).
- **Logo (bozza):** una S tracciata come una strada, con una linea sola e continua, che finisce nel punto dove si parcheggia. Due colori più il bianco; leggibile a 24 px; versioni su fondo scuro e chiaro in `16-grafica.md`.
- **Nota:** "Mi" lega il nome a Milano. Per altre città (D-013) servirà decidere se tenere il nome o declinarlo.

## D-034 — Vista live: regola A
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore, subordinata alla conferma del red team (T-047)
- **Scelta:** chi ha già contribuito in una zona entra subito nel dato live; i nuovi contributori entrano ogni 30 minuti. Resta l'aggiornamento ogni 5 minuti.

## D-035 — Versione web di SostaMi (computer e telefono)
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore (vuole usarla da computer e da iPhone); prima versione pubblicata come pagina privata
- **Fatto:** `web/app_template.html` e `scripts/build_webapp.py` producono un'app in una sola pagina con la **mappa vera di Milano** disegnata dai dati del Comune (strade con nome, edifici, verde, acqua, ferrovie, aree di sosta, parcheggi in struttura), ricerca delle vie, vista live e altri orari, veicolo, sosta salvata con timer, segnalazione dell'esito, collegamenti di navigazione, pagina privacy. Link: https://claude.ai/artifact/RCK6XaPgv7oTuTKun7Wk87
- **Limiti di questa forma (pagina dentro Claude):** è privata del fondatore finché non la condivide; non può leggere la posizione GPS; non può caricare una mappa di sfondo da altri siti; non comunica con il nostro servizio, quindi le segnalazioni restano sul dispositivo e la mappa reale resta grigia. I colori si vedono solo con "Mostra esempio", dichiarato finto.
- **Passo successivo proposto:** pubblicare la stessa app come sito vero (per esempio GitHub Pages, gratuito): avrebbe un link pubblico, si installa sulla schermata Home dell'iPhone, può usare il GPS e collegarsi al servizio. Pubblicare è una decisione del fondatore e richiede prima la verifica del red team (T-047), la DPIA firmata e un servizio online (T-030).
- **Conseguenza per la beta:** la versione web può sostituire o affiancare l'app Android: nessuno store, nessuna installazione, funziona su iPhone, Android e computer.

## D-036 — La beta è un sito web; pubblicazione su GitHub Pages
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore (forma A; pubblicazione: sì)
- **Scelta:** la beta è la versione web di SostaMi, raggiungibile da un link pubblico gratuito, su iPhone, Android e computer. App Android e store dopo.
- **Preparato:** cartella `site/` (app completa, icone, manifesto per l'aggiunta alla schermata Home) e flusso `.github/workflows/pages.yml` che la pubblica. Il pulsante "Dove sono" usa il GPS solo sul dispositivo, a richiesta.
- **Cosa deve fare il fondatore:** nelle impostazioni del repository, Pages → Source: "GitHub Actions"; se la pubblicazione è limitata al ramo principale, consentire il ramo di lavoro o unirlo. Indirizzo atteso: `https://giovanni0702.github.io/Project/`.
- **Cosa si può pubblicare subito:** questa versione non raccoglie né invia dati, quindi non richiede la DPIA. La raccolta delle segnalazioni si attiva solo dopo T-047, DPIA firmata e servizio online (T-044, T-030).
- **Da sapere:** il repository è **pubblico**: documenti, strategie e bozze sono già visibili a chiunque. Se non è voluto, va reso privato (ma GitHub Pages gratuito richiede un repository pubblico: in quel caso il sito va in un repository separato).
- **Conseguenze:** niente rilevamento automatico in background (impossibile in un sito); D-017 (beta solo Android) è superata; i vincoli Google Play e App Store si rinviano.

## D-037 — Posti totali, occupati e liberi: modello matematico, senza dati Google
- **Data:** 2026-11-14
- **Stato:** obiettivo deciso dal fondatore; metodo scelto dal team (T-049, in corso)
- **Perché non Google Maps:** i termini letti alla fonte vietano di estrarre, conservare o usare i loro contenuti per crearne di propri (D-004); inoltre Google non espone posti liberi né auto in sosta. Usarli esporrebbe il progetto alla chiusura dell'accesso e a contestazioni, soprattutto in vista di una cessione del dato (D-013).
- **Metodo:** (1) capacità per tratto = aree di sosta mappate + stima della sosta lungo il marciapiede dalla lunghezza dei tratti; (2) domanda dal movimento reale disponibile: residenti e auto per quartiere, ingressi in Area C, attività per quartiere; (3) teoria delle code: sistema a c posti con arrivi e durate di sosta variabili nel tempo (formule di Erlang B e C), da cui posti occupati, posti liberi e probabilità di trovare posto entro 5 minuti, ciascuno con intervallo di incertezza; (4) calibrazione bayesiana con le segnalazioni reali.
- **Onestà:** finché mancano le segnalazioni, i numeri sono stime del modello non verificate e l'app lo dichiara.

## D-038 — Repository privato, sito in un repository separato
- **Data:** 2026-11-14
- **Stato:** decisa dal fondatore
- **Scelta:** il repository del progetto diventa privato; il sito si pubblica da un repository pubblico separato che contiene solo i file di `site/` (nessun documento, nessun codice del modello).
- **Azioni del fondatore** (gli agenti non creano repository né cambiano la visibilità):
  1. creare un repository pubblico vuoto, per esempio `sostami`;
  2. in quel repository: Settings → Pages → Source: "GitHub Actions";
  3. rendere privato `Project`: Settings → General → Danger Zone → Change visibility;
  4. dare a Claude l'accesso al nuovo repository (impostazioni dell'app GitHub di Claude) e dirlo in chat.
- **Poi fa il team:** copia `site/` nel nuovo repository (il flusso di pubblicazione è già in `site/.github/workflows/pages.yml`) e verifica che l'indirizzo risponda. Indirizzo atteso: `https://giovanni0702.github.io/sostami/`.
- **Nota:** la cronologia pubblica già copiata o indicizzata da terzi non si può ritirare; rendere privato il repository vale da quel momento in poi.
