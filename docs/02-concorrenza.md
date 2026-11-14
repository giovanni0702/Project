# 02 — Analisi della concorrenza

Stato: **bozza iniziale** basata su una prima ricerca web (giugno–novembre 2026). Va approfondita dal `competitor-analyst` prima di ogni iterazione. Le informazioni marcate **[verificare]** non sono confermate sulle app o sui siti ufficiali.

## 1. Mappa dei competitor

| Player | Tipo | Cosa fa | Previsione posti liberi | Fonte / stato |
|---|---|---|---|---|
| **EasyPark (Find & Park)** | Pagamento sosta + navigazione | Pagamento strisce blu. Funzione Find & Park che stima i posti liberi lungo il percorso, con colori verde→grigio | Sì, su strisce blu | Lancio a Milano nel 2019 (fonte: Quotidiano.net). Funzionamento attuale a Milano **[verificare]** |
| **FindPark** | App parcheggio | Presentata come app che rende il parcheggio "più facile" a Milano | Da verificare | Articolo SicurAuto **[verificare funzioni]** |
| **myCicero** | Navigazione + sosta | Mostra spazi liberi su strada con una funzione di navigazione "Find" | Sì, da verificare | Guida di Tom's Hardware **[verificare]** |
| **Parkopedia** | Mappa parcheggi | Mostra parcheggi su mappa, soprattutto garage | No per strada (per garage sì, in parte) | Fastweb **[verificare]** |
| **Parclick** | Prenotazione e pagamento | Prenota garage, paga strisce blu a Milano | No | Sito Parclick |
| **Telepass** | Pagamento sosta | Pagamento parcheggi a Milano centro | No | Sito Telepass |
| **MooneyGo** | Pagamento sosta, abbonamenti | App autorizzata da ATM per abbonamenti | No | Sicurauto / Tom's Hardware |
| **DropTicket** | Pagamento sosta | Pagamento strisce blu | No | Sicurauto |
| **Google Maps** | Navigazione | Indicatore "difficoltà parcheggio" (Limited / Medium / Easy) da dati storici, dal 2017 | Stima storica, non in tempo reale | Blog Google Research 2017 |
| **INRIX** | B2B, piattaforma predittiva | Predice disponibilità all'orario di arrivo, previsioni fino a 7 giorni. 22.000 città dichiarate | Sì, molto avanzata | Comunicati INRIX (giugno 2026). Accuratezza ~99% **auto-dichiarata** |
| **SpotAngels** | Crowdsourcing + dashcam | "Waze del parcheggio", raccolta da membri della community | Sì (storico) | Finanziamento 2018. Stato attuale **[verificare]** |
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
