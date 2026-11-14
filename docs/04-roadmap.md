# 04 — Roadmap a iterazioni

Ogni iterazione produce qualcosa di usabile e misurabile, e ha un criterio di **uscita** e uno di **abbandono**.

## Iterazione 0 — Fondamenta (chiusa il 2026-11-14, con conferma del fondatore)
- [x] Regole, team di agenti, documenti 01–13, board, `make check`, CI
- [x] Prima verifica di open data, termini Google, store, concorrenti, costi (parziale: → `STATO.md`)
- [x] Verifiche T-001–T-003 rifatte sui testi ufficiali; T-004 (concorrenti sugli store) passa all'iterazione 1
- [x] Stack (D-003) e mappa (D-010) confermati dal fondatore; nessuna spesa fino al lancio (D-014)

**Uscita:** documenti approvati dal fondatore, board pronto.

## Iterazione 1 — Dati, modello v0 (backend e pagina web interna) — in corso
- Rete stradale e sosta da OpenStreetMap (attribuzione ODbL); dataset del Comune verificati.
- Configurazione della città (`cities/milano`), secondo D-013: nessun valore di Milano nel codice.
- Griglia H3 su tutta Milano; regole di sosta per cella (tariffe, orari, lavaggio strade se disponibili).
- Modelli 1 e 2 di [`09-modello.md`](09-modello.md); pubblicazione statica (D-011); pagina interna con mappa.
- Test di calibrazione su dati sintetici, etichettati come test tecnici.
- Tutto in locale, senza servizi a pagamento (D-014).
- Piano di validazione senza rilevazioni sul campo (T-021, D-015).

**Uscita:** test automatico che fallisce se il nucleo contiene valori specifici di Milano; ≥ 90% delle strade con sosta coperte da una stima; pipeline riproducibile con un comando; `make check` verde; nessun segreto o dato personale nel repository.
**Limite dichiarato:** a fine iterazione il prior non è validato su dati reali.

## Iterazione 2 — Beta chiusa (centro)
- App Flutter IT/EN: onboarding con consenso, mappa, affidabilità, contributi a un tap.
- Regole della zona e avviso lavaggio strade (T-011); "ricorda dove ho parcheggiato" e timer (T-012); funzionamento offline (T-016); contatore locale (T-015); regole di sicurezza alla guida (T-014).
- Dati reali e attuali secondo D-016: tap, "ricorda dove ho parcheggiato", Bluetooth dell'auto dopo DPIA, missioni, griglia pubblicata ogni 15 minuti.
- 10–20 tester, solo Android, installazione diretta, server su piano gratuito (D-017).
- Missioni di copertura per i tester e quota di esiti riservata alla validazione.

**Uscita:** ≥ 500 esiti reali in centro; calibrazione misurata e documentata; app compresa in meno di 1 minuto; ≥ 30% dei tester contribuisce almeno una volta a settimana; privacy policy e DPIA pronte per la firma; test di re-identificazione superato.
**Abbandono o cambio di rotta:** se i tester non contribuiscono, si rivede il meccanismo di contributo prima di qualsiasi lancio. Se sugli esiti reali il prior non fa meglio del caso, il prodotto principale diventa "regole di sosta e lavaggio strade" e il modello si rivede.

## Iterazione 3 — Pilota pubblico
- Conto completo dei costi presentato al fondatore prima di qualsiasi attivazione (D-014).
- Release sugli store, tutto il Comune, strisce bianche. Google Maps come motore della mappa, se costi e termini lo permettono (D-010).
- Nome e verifica marchi; marketing e ASO; opzioni di ricavo presentate al fondatore (T-017).

**Uscita:** rating ≥ 4,0 (da confermare); calibrazione entro tolleranza; nessun incidente privacy aperto.
**Abbandono:** calibrazione fuori tolleranza per due pubblicazioni consecutive → si sospende la crescita e si torna al modello.

## Iterazione 4 — Prodotto completo
- Parcheggi di struttura e di interscambio; "Piano B" (T-013); previsione all'orario di arrivo.
- CarPlay / Android Auto; eventuali partnership per il pagamento (da valutare).
- Prova a secco: configurare una seconda città solo con dati aperti, senza lanciarla, per misurare quanto il nucleo è davvero indipendente da Milano.

## Oltre il pilota (visione, D-013)
Ogni passo richiede una decisione del fondatore e la **verifica di prontezza**.

| Passo | Contenuto | Si apre quando |
|---|---|---|
| 5 — Seconda città italiana | Prima prova che una città è configurazione; misura di tempo e costo per aggiungerla | Milano calibrata entro tolleranza e contributi stabili |
| 6 — Più città italiane | Procedura ripetibile; prior trasferito tra città | Seconda città aggiunta senza modifiche al nucleo |
| 7 — Altri paesi | Lingue, regole e norme locali; residenza dei dati | Procedura stabile; parere legale per paese |
| 8 — Dato in licenza e integrazioni | API per terzi, prove di calibrazione, proposta alle app di mappe | Più città calibrate; origine dei dati e licenze in ordine |

**Verifica di prontezza per una nuova città:** fonti e licenze verificate · regole di sosta mappate · copertura OSM sufficiente · prior calcolato · piano per i primi contributi · costo stimato · parere di `privacy-compliance`.

## Chiusura di un'iterazione
1. Metriche di uscita raggiunte, o fallimento documentato.
2. Approvazione di `privacy-compliance`.
3. `02-concorrenza.md` aggiornato.
4. Suite completa verde; task `Fatto` spostati in `archivio/`.
5. Retrospettiva di 3 righe in `STATO.md`: cosa tenere, cosa cambiare, dove si sono sprecati token.
6. Conferma del fondatore.
