# 04 — Roadmap a iterazioni

Ogni iterazione produce qualcosa di usabile e misurabile, e ha un criterio di **uscita** e uno di **abbandono**.

## Iterazione 0 — Fondamenta (in chiusura)
- [x] Regole, team di agenti, documenti 01–13, board, `make check`, CI
- [x] Prima verifica di open data, termini Google, store, concorrenti, costi (parziale: → `STATO.md`)
- [ ] Verifiche bloccate dalla rete completate (T-001–T-004)
- [ ] Stack (D-003) e mappa (D-010) confermati dal fondatore

**Uscita:** documenti approvati dal fondatore, board pronto.

## Iterazione 1 — Dati, modello v0, prova dell'ipotesi (backend e pagina web interna)
- Rete stradale e sosta da OpenStreetMap (attribuzione ODbL); dataset del Comune verificati.
- Griglia H3 su tutta Milano; regole di sosta per cella (tariffe, orari, lavaggio strade se disponibili).
- Modelli 1 e 2 di [`09-modello.md`](09-modello.md); pubblicazione statica (D-011); pagina interna con mappa.
- Test di calibrazione su dati sintetici, etichettati come test tecnici.
- **Prova a basso costo dell'ipotesi:** protocollo di rilevazione sul campo e traccia per 5 interviste (T-021). Le esegue il fondatore.

**Uscita:** ≥ 90% delle strade con sosta coperte da una stima; pipeline riproducibile con un comando; `make check` verde; nessun segreto o dato personale nel repository.
**Abbandono o cambio di rotta:** se sul campo il prior non fa meglio del caso, il prodotto principale diventa "regole di sosta e lavaggio strade" e il modello si rivede.

## Iterazione 2 — Beta chiusa (centro)
- App Flutter IT/EN: onboarding con consenso, mappa, affidabilità, contributi a un tap.
- Regole della zona e avviso lavaggio strade (T-011); "ricorda dove ho parcheggiato" e timer (T-012); funzionamento offline (T-016); contatore locale (T-015); regole di sicurezza alla guida (T-014).
- Rilevamento automatico solo opzionale e solo dopo DPIA.
- 10–30 tester via TestFlight e Play internal testing.

**Uscita:** ≥ 500 esiti reali in centro; calibrazione misurata e documentata; app compresa in meno di 1 minuto; ≥ 30% dei tester contribuisce almeno una volta a settimana; privacy policy e DPIA pronte per la firma; test di re-identificazione superato.
**Abbandono:** se i tester non contribuiscono, si rivede il meccanismo di contributo prima di qualsiasi lancio.

## Iterazione 3 — Pilota pubblico
- Release sugli store, tutto il Comune, strisce bianche.
- Nome e verifica marchi; marketing e ASO; opzioni di ricavo presentate al fondatore (T-017).

**Uscita:** rating ≥ 4,0 (da confermare); calibrazione entro tolleranza; nessun incidente privacy aperto.
**Abbandono:** calibrazione fuori tolleranza per due pubblicazioni consecutive → si sospende la crescita e si torna al modello.

## Iterazione 4 — Prodotto completo
- Parcheggi di struttura e di interscambio; "Piano B" (T-013); previsione all'orario di arrivo.
- CarPlay / Android Auto; eventuali partnership per il pagamento (da valutare).
- Architettura pronta per altre città (decisione separata del fondatore).

## Chiusura di un'iterazione
1. Metriche di uscita raggiunte, o fallimento documentato.
2. Approvazione di `privacy-compliance`.
3. `02-concorrenza.md` aggiornato.
4. Suite completa verde; task `Fatto` spostati in `archivio/`.
5. Retrospettiva di 3 righe in `STATO.md`: cosa tenere, cosa cambiare, dove si sono sprecati token.
6. Conferma del fondatore.
