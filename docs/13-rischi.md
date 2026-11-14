# 13 — Registro dei rischi

P = probabilità, I = impatto (A alta, M media, B bassa). Rivisto da `ops-watchdog` a ogni ciclo. Un rischio che cambia livello apre un task.

| Id | Rischio | P | I | Mitigazione | Proprietario |
|---|---|---|---|---|---|
| R-01 | **Partenza a freddo:** senza utenti non ci sono dati, senza dati l'app non serve | A | A | Valore dal giorno zero con regole di sosta e lavaggio strade (T-011); contributo come effetto di "ricorda dove ho parcheggiato" (T-012) | product-manager |
| R-02 | Il prior non fa meglio del caso | M | A | Rilevazioni sul campo in iterazione 1 (T-021); criterio di abbandono in `04-roadmap.md` | data-scientist |
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
