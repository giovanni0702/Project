# 02 — Analisi della concorrenza

Stato: **bozza aggiornata il 2026-11-14 (T-004)**, ricerca web senza accesso agli store. Va approfondita dal `competitor-analyst` prima di ogni iterazione. Le informazioni marcate **[verificare]** non sono confermate sulle app o sui siti ufficiali.

## 1. Mappa dei competitor

| Player | Tipo | Cosa fa | Previsione posti liberi | Fonte / stato |
|---|---|---|---|---|
| **EasyPark (Find & Park)** | Pagamento sosta + navigazione | Pagamento strisce blu (a Milano dal 2015). Find & Park: strade colorate (verde, giallo, arancione, grigio scuro) con probabilità; tap sulla strada per il dettaglio. Risparmio "200 g CO2 e 4 min a sosta" dichiarato dal competitor | Sì, su strisce blu (stima) | Lancio Find & Park a Milano giugno 2019 (Quotidiano.net). Pagina help EasyPark ancora attiva, consultata 2026-11-14 (via ricerca; pagina non letta per intero). Non verificato in app che funzioni oggi a Milano **[verificare in app]** |
| **FindPark** | App parcheggio | L'articolo SicurAuto "FindPark attivo a Milano" sembra riferirsi a Find & Park di EasyPark (stessa funzione, stesso lancio), non a un'app distinta. Nessuna app autonoma "FindPark" trovata negli store | Vedi EasyPark | SicurAuto, ricerca 2026-11-14. Probabile errore di nome, non un concorrente separato **[verificare titolo articolo]** |
| **myCicero / MooneyGo** | Pagamento sosta + mobilità | Rinominata MooneyGo (ex myCicero). Funzione "FIND" citata come aiuto a trovare parcheggi liberi su strada (money.it); oltre 60 località (fonte datata). Nessuna fonte descrive il metodo né la copertura a Milano | Citata, non documentata **[verificare in app]** | money.it, Tom's Hardware, Aranzulla; ricerca 2026-11-14 |
| **Parkopedia** | Mappa parcheggi + dati B2B | Consumer: soprattutto garage. B2B: dichiara "probabilità di trovare parcheggio" per segmento stradale con dati fusi (rilevamenti, sensori, transazioni, ML), 90 mln di posti. Copertura stradale in Italia/Milano non trovata | Sì in B2B (dichiarato); consumer su strada Milano non confermato **[verificare]** | business.parkopedia.com (analytics, blog), ricerca 2026-11-14 |
| **Parclick** | Prenotazione e pagamento | Prenota garage, paga strisce blu a Milano | No | Sito Parclick |
| **Telepass** | Pagamento sosta | Pagamento parcheggi a Milano centro | No | Sito Telepass |
| **MooneyGo** | Pagamento sosta, abbonamenti | App autorizzata da ATM per abbonamenti | No | Sicurauto / Tom's Hardware |
| **DropTicket** | Pagamento sosta | Pagamento strisce blu | No | Sicurauto |
| **Google Maps** | Navigazione | Indicatore "difficoltà parcheggio" (Limited / Medium / Easy) da dati storici, dal 2017 | Stima storica, non in tempo reale | Blog Google Research 2017 |
| **INRIX** | B2B, piattaforma predittiva | Predice disponibilità all'orario di arrivo, previsioni fino a 7 giorni. 22.000 città dichiarate | Sì, molto avanzata | Comunicati INRIX (giugno 2026). Accuratezza ~99% **auto-dichiarata** |
| **SpotAngels** | Crowdsourcing + dashcam | Attiva: listing App Store "SpotAngels Parking & Gas" con avvisi per pulizia strade/regole, salvataggio posizione auto (Bluetooth o manuale). Focus USA (NYC, Chicago, SF). Presenza in Italia/Milano non trovata **[verificare]**. Accuratezza ">95%" dichiarata dal competitor | Sì (storico), solo città USA | App Store listing e Product Hunt, ricerca 2026-11-14 |
| **Google Maps (assistente parcheggio)** | Navigazione | Indicatore "Posti limitati / Parcheggio facile" attivo anche in Italia | Stima storica | SicurAuto, ricerca 2026-11-14 (data articolo non letta **[verificare]**) |
| **PuliAMO** | Avvisi pulizia strade | App citata da un blog per notifiche sugli interventi di pulizia programmati. Non confermata su Comune/AMSA né sugli store | No | parkingmycar.it, 2026-11-14 **[verificare esistenza e copertura]** |
| **ParkEz / SpotGenius** | App consumer | Probabilità di trovare posto (es. 4 livelli) | Sì | Store listing **[verificare]** |
| **Ricerca MIT (feb. 2026)** | Ricerca accademica | Navigazione "parking-aware" con probabilità. Osservazioni crowdsourced con errore circa 7% | Conferma la fattibilità | Comunicato MIT |

## 2. Lettura del mercato

- **Esiste già un segmento "probabilità di parcheggio"**, ma è coperto da grandi player (INRIX per B2B, EasyPark nelle strisce blu) e da app di nicchia.
- **Il pagamento è il modello dominante in Italia.** Chi paga la sosta resta nell'app, quindi trovare posto è un "secondo" prodotto, non il core.
- **Il crowdsourcing è la strada più promettente.** È confermato dalla ricerca MIT e da SpotAngels, ma SpotAngels è rimasta indietro sul mercato.
- **Google Maps non dà un dato in tempo reale** sui posti liberi. È un vuoto che un'app dedicata può coprire, a condizione di rispettare i termini d'uso.
- **Milano è un mercato forte per la sosta:** la sosta a pagamento è in espansione e si parla di eliminare parcheggi gratuiti in alcune zone (fonte: stampa, 2025). È un contesto che aumenta il bisogno, ma va verificato.

## 3. Punti di forza e debolezza dei competitor

### EasyPark
- **Forza:** utenti già abituati, pagamento integrato, funzione Find & Park già pensata per Milano.
- **Debolezza:** Find & Park non è sempre evidente nell'app; la previsione dipende dalle strisce blu; la UX è orientata al pagamento, non alla ricerca del posto.
- **Cosa copiare:** la colorazione verde→grigio lungo il percorso è semplice e leggibile.
- **Cosa evitare:** mescolare pagamento e ricerca nella stessa schermata.

### Google Maps
- **Forza:** utenti enormi, navigazione perfetta, dati di traffico.
- **Debolezza:** l'indicatore di difficoltà è storico, a tre livelli, e non dice quanti posti restano. Non c'è un contributo dell'utente sui posti liberi.
- **Cosa copiare:** la semplicità dei tre livelli.
- **Cosa evitare:** un'indicazione senza spiegazione dell'affidabilità.

### INRIX
- **Forza:** scala globale, previsioni fino a 7 giorni, integrazione con veicoli connessi.
- **Debolezza:** B2B, non pensata per l'automobilista singolo; accuratezza auto-dichiarata; probabilmente costosa e non disponibile come prodotto consumer.
- **Cosa copiare:** la previsione all'orario di arrivo (ETA).
- **Cosa evitare:** il linguaggio tecnico verso l'utente finale.

### Parkopedia / Parclick / Telepass / MooneyGo / DropTicket
- **Forza:** pagamento e prenotazione consolidati, forte base utenti.
- **Debolezza:** nessuna previsione di disponibilità in tempo reale su strada.
- **Opportunità:** possono essere partner (integrazione del pagamento) nelle fasi successive.

### SpotAngels
- **Forza:** modello crowdsourced già testato, dashcam come fonte dati.
- **Debolezza:** dashcam = privacy molto complessa in Europa; presenza attuale incerta.
- **Cosa evitare:** raccolta video. Noi usiamo solo eventi anonimi e aggregati (vedi `03-privacy.md`).

### Recensioni e temi ricorrenti (ricerca 2026-11-14)
Gli host degli store (apps.apple.com, play.google.com) non erano raggiungibili dalla sessione: i temi vengono da Trustpilot, Altroconsumo e report terzi, quindi sono indicativi e vanno confermati sugli store **[verificare]**.
- **EasyPark Italia:** (1) multa ricevuta nonostante sosta pagata, sospetto errore di posizione/sessione (Trustpilot, Altroconsumo, 2026); (2) sessioni che non si chiudono e notifiche inaffidabili; (3) pulsante/funzioni che smettono di funzionare dopo aggiornamenti. Nessuna recensione citata su Find & Park.
- **MooneyGo (ex myCicero):** (1) affidabilità tecnica e UX da migliorare (Kimola, sintesi recensioni Google Play); (2) credito prepagato con residui non usati, vs app che addebitano l'importo esatto (forum fibra.click); (3) utenti che preferiscono EasyPark per le strisce blu.
- **Implicazione:** il tema dominante è la fiducia (pagato ma multato), non la ricerca del posto. Nessuno cita "posto non trovato" o "troppi annunci".

### Regole di zona, avviso lavaggio strade, "dove ho parcheggiato" a Milano
- Nessun competitor trovato offre a Milano regole di zona più avviso pulizia strade integrati con la probabilità di posto. Il calendario pulizia è su blog (parkingmycar.it) e cartelli; PuliAMO non confermata.
- SpotAngels offre avvisi pulizia e salvataggio posizione, ma in città USA; a Milano non confermato.
- "Ricorda dove ho parcheggiato" non trovato su app milanesi (ricerca 2026-11-14).
- **Spazio libero probabile**, ma verificare in app prima di dichiararlo.

### Nuovi concorrenti a Milano
Nessuna app o startup con previsione di posti su strada a Milano trovata (ricerca 2026-11-14). ParkingMyCar (Umbria, 2019) prenota garage. Sperimentazione comunale a San Siro: prenotazione su aree strutturate, fino al 31/12/2026.

## 4. Il nostro spazio (ipotesi da validare)

Nessun competitor, per quanto emerso finora, combina tutti questi elementi:

1. **Probabilità per zona e per orario di arrivo**, non solo mappa o pagamento.
2. **Contributo semplice e anonimo degli utenti** con un tap, senza video.
3. **Focus su Milano intera**, con dati e spiegazioni locali (zone, tariffe, orari).
4. **Due lingue dal lancio**, con UX molto semplice.
5. **Privacy come differenziatore** (dati aggregati, nessun video, nessun tracking pubblicitario).

**Ipotesi da verificare nella iterazione 1:** un utente medio di Milano riesce a capire e usare l'app senza tutorial. Va testato con utenti reali nell'iterazione 2.

## 5. Piano di aggiornamento

Il `competitor-analyst` deve:
- verificare sugli store (App Store e Google Play) le funzioni reali di EasyPark, FindPark, myCicero, Parkopedia e ParkEz;
- verificare se Find & Park funziona oggi a Milano e con quale copertura;
- raccogliere recensioni recenti (ultimi 12 mesi) e segnalare i temi ricorrenti: "posto non trovato", "dati vecchi", "troppi annunci";
- aggiornare la tabella a ogni iterazione e aprire task per le novità rilevanti.

## 6. Fonti

- Quotidiano.net, *Find & Park a Milano* (2019): https://motori.quotidiano.net/news/find-park-milano-parcheggio.htm
- SicurAuto, *FindPark attivo a Milano*: https://www.sicurauto.it/news/attualita-e-curiosita/findpark-attivo-a-milano-il-parcheggio-piu-facile-via-app/
- SicurAuto, *Strisce blu Milano 2026*: https://www.sicurauto.it/news/traffico-e-viabilita/strisce-blu-milano-2026-orari-tariffe-e-norme/
- Google Research, *Using Machine Learning to Predict Parking Difficulty* (2017): https://www.research.google/blog/using-machine-learning-to-predict-parking-difficulty/
- INRIX, *Predictive and accurate parking intelligence*: https://inrix.com/press-releases/inrix-sets-the-standard-for-predictive-and-accurate-parking-intelligence/
- MIT, *Parking-aware navigation system* (2026): https://lidspreview.mit.edu/news/parking-aware-navigation-system-could-prevent-frustration-and-emissions
- Parclick, *Abbonamento di parcheggio a Milano*: https://parclick.it/info/abbonamento-parcheggio-milano/
- Telepass, *Parcheggi Milano centro*: https://www.telepass.com/en/consumer/services/parkings/milano-centro
- EasyPark, *Find & Park*: https://www.easypark.com/en-cy/help/parking/parking-find--27429871361820
- Fastweb, *App per trovare parcheggio*: https://www.fastweb.it/smartphone-e-gadget/app-trovare-parcheggio
- Tom's Hardware, *Come usare MooneyGo*: https://www.tomshw.it/automotive/come-usare-mooneygo-mycicero
- Parkopedia Business, *Why Predictions Beat Real-Time*: https://business.parkopedia.com/blog/why-predictions-beat-real-time-every-time (consultata 2026-11-14)
- money.it, *Come pagare il parcheggio da app*: https://www.money.it/Come-pagare-parcheggio-da-app-senza-contanti-carta (2026-11-14)
- Kimola, *MooneyGo Google Play reviews*: https://kimola.com/reports/explore-user-insights-enhance-your-strategy-with-our-report-google-play-it-152951 (2026-11-14)
- SpotAngels App Store: https://apps.apple.com/us/app/id897809583 (2026-11-14)
- Trustpilot EasyPark Italia: https://se.trustpilot.com/review/easypark.com/it-it (2026-11-14)
- ParkingMyCar, *Pulizia strade Milano 2026*: https://www.parkingmycar.it/blog/pulizia-strade-milano/ (2026-11-14)
- SicurAuto, *Google Maps assistente parcheggio in Italia*: https://www.sicurauto.it/ricambi-e-accessori/google-maps-lassistente-al-parcheggio-e-ora-attivo-anche-in-italia/ (2026-11-14)
