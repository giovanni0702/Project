# 13 — Registro dei rischi

P = probabilità, I = impatto (A alta, M media, B bassa). Rivisto da `ops-watchdog` a ogni ciclo. Un rischio che cambia livello apre un task.

| Id | Rischio | P | I | Mitigazione | Proprietario |
|---|---|---|---|---|---|
| R-01 | **Partenza a freddo:** senza utenti non ci sono dati, senza dati l'app non serve | A | A | Valore dal giorno zero con regole di sosta e lavaggio strade (T-011); contributo come effetto di "ricorda dove ho parcheggiato" (T-012) | product-manager |
| R-02 | Il prior non fa meglio del caso, e lo scopriamo solo in beta (nessuna rilevazione sul campo, D-015) | M | A | Affidabilità bassa dichiarata; validazione sugli esiti dei tester (T-021); criterio di abbandono in iterazione 2 | data-scientist |
| R-03 | Mancano dati aperti su stalli e regole di sosta | M | A | Verifica T-001; ripiego su OSM e rilevazioni proprie | data-engineer |
| R-04 | I tester non contribuiscono | M | A | Contributo a un tap e come effetto di funzioni utili; soglia di abbandono in iterazione 2 | ux-designer |
| R-05 | Re-identificazione dagli aggregati | B | A | Soglia k, pubblicazione a intervalli fissi, test di re-identificazione (T-018) | privacy-compliance |
| R-06 | Rifiuto in revisione store per la localizzazione | M | M | Requisiti in `10-release.md`; background solo opzionale | release-manager |
| R-07 | Un concorrente con più dati copre Milano | M | M | Differenziarsi su privacy, onestà dei numeri e regole locali; aggiornamento a ogni iterazione | competitor-analyst |
| R-08 | Segnalazioni false alterano le stime | M | M | Antiabuso in `12-sicurezza.md` (T-019) | backend-engineer |
| R-09 | Uso dell'app alla guida | M | A | Nessuna interazione in movimento, richieste solo a veicolo fermo (T-014) | ux-designer |
| R-10 | Costi che crescono con gli utenti | B | M | Griglia statica da CDN, mappa senza costi per richiesta (D-010, D-011) | backend-engineer |
| R-11 | Distorsione di chi segnala | A | M | Insieme di validazione sul campo; limiti dichiarati in `09-modello.md` | data-scientist |
| R-12 | Un solo fondatore: tempo e continuità | A | M | `STATO.md` come passaggio di consegne; task piccoli con budget | ceo-orchestrator |
| R-13 | Vincoli sui dati o sui marchi di terzi (Google, nome del prodotto) | M | M | Nessun dato Google nel modello (D-004); verifica marchi prima del nome | privacy-compliance |
| R-14 | Regole di sosta mostrate ma sbagliate o non aggiornate | M | A | Data della fonte visibile; avviso "vale la segnaletica"; aggiornamento automatico della fonte | data-engineer |
| R-15 | Costruire per il mondo prima di aver dimostrato Milano (complessità e costi prematuri) | M | A | D-013: solo regole di costruzione, nessuna infrastruttura in più; espansioni con verifica di prontezza | ceo-orchestrator |
| R-16 | La licenza ODbL limita la cessione a terzi di dati derivati da OSM | M | A | Usare dati del Comune come variabili dove possibile; OSM come base cartografica; eventuale tabella derivata da OSM pubblicata a parte; parere legale prima di qualsiasi proposta commerciale (T-024) | privacy-compliance |
| R-17 | Le grandi app di mappe non integrano dati di terzi, o li sviluppano da sole | A | M | Il prodotto deve reggersi da solo; il dato in licenza è un'opzione, non il piano unico | product-manager |
| R-18 | Ogni città ha regole e fonti diverse: costo di ingresso alto | A | M | Adattatori per fonte; OSM come base comune; misura del costo sulla seconda città | data-engineer |
| R-19 | Senza spesa prima del lancio (D-014) la beta su iPhone non è possibile e i piani gratuiti possono non bastare | M | M | Beta da Android con installazione diretta; verifica dei piani gratuiti prima dell'iterazione 2 | release-manager |
| R-20 | In beta i tester sono troppo pochi per superare la soglia k: i dati reali non compaiono sulla mappa | A | A | Beta concentrata in poche zone, celle e fasce più larghe (T-029); missioni | data-scientist |
| R-21 | Piani gratuiti del server sospesi o lenti durante la beta | M | M | Verifica sulle pagine ufficiali (T-030); griglia statica scaricata anche a server fermo | backend-engineer |
| R-22 | Rilevamento automatico: falsi parcheggi (garage, passeggeri, mezzi pubblici), batteria, rifiuto su Google Play per la posizione in background | A | A | Conferma a un tap, zone escluse, soglia di batteria, prova in beta fuori dagli store; dichiarazione Play preparata prima del lancio (D-018) | mobile-engineer |
| R-23 | La mappa per strada suggerisce una precisione che i dati non hanno | A | M | Stima per cella dichiarata nella scheda; affidabilità sempre visibile; differenze tra strade solo da caratteristiche verificate (D-021) | data-scientist |
| R-24 | Correzioni per taglia e stima per le moto basate su ipotesi | A | M | Etichettate come indicative; sostituite da valori appresi; fonte degli stalli moto (T-036) | data-scientist |