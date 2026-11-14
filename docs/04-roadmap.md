# 04 — Roadmap a iterazioni

Regola: **ogni iterazione deve produrre qualcosa di usabile e misurabile**. Nessuna iterazione è "prodotto completo". Il prodotto completo arriva dopo iterazioni 3 e 4.

## Iterazione 0 — Fondamenta (in corso)
**Obiettivo:** avere la struttura di progetto, il team di agenti e la base strategica.

- [x] Regole del progetto (`CLAUDE.md`)
- [x] Team di agenti con ruoli e gerarchia
- [x] Visione, scope, concorrenza, privacy, dati
- [ ] Verifica del board dei task e primo ciclo di `ops-watchdog`
- [ ] Decisione dello stack (D-003) confermata dal fondatore

**Uscita:** documenti approvati, board pronto, primi task assegnati.

## Iterazione 1 — Dati e modello v0 (solo backend e web interno)
**Obiettivo:** dimostrare che il modello di probabilità funziona su Milano, anche con dati limitati.

- Caricamento della rete stradale e dei parcheggi da OpenStreetMap (con attribuzione ODbL).
- Ricerca e acquisizione di dataset aperti del Comune di Milano su sosta, zone e tariffe.
- Griglia H3 su tutta Milano.
- Modello v0: prior storico per cella e fascia oraria, aggiornamento bayesiano, decadimento temporale, stima P(posto entro t) = 1 − e^(−λt).
- API di base e pagina web interna per visualizzare la mappa e validare i risultati.
- Test di calibrazione su dati simulati (**solo per test tecnici, non come prova di accuratezza**).

**Metriche di uscita:**
- Copertura: almeno il 90% delle strade con parcheggio stimato su tutta Milano.
- Pipeline dati riproducibile e documentata.
- Nessuna chiave o dato personale nel repository.

## Iterazione 2 — App beta chiusa (Milano centro)
**Obiettivo:** app utilizzabile da beta tester, con raccolta reale di segnalazioni.

- App Flutter iOS + Android, IT/EN, onboarding con consenso chiaro.
- Mappa con zone colorate e indicatore di affidabilità.
- Flusso "ho parcheggiato / ho lasciato il posto" manuale.
- Modalità automatica opzionale (solo se la DPIA la approva).
- Distribuzione via TestFlight e Play internal testing a 10–30 tester.
- Raccolta di eventi reali per calibrare il modello.

**Metriche di uscita:**
- Almeno 500 eventi reali raccolti in centro.
- Calibrazione misurata e pubblicata nel documento di iterazione.
- Tempo di comprensione dell'app per un nuovo utente sotto 1 minuto (test con tester reali).
- Privacy policy e DPIA firmate dal fondatore.

## Iterazione 3 — Pilota pubblico Milano
**Obiettivo:** lancio pubblico su App Store e Play Store, solo per Milano.

- Release su store con etichette privacy e localizzazione completa.
- Copertura estesa a tutto il Comune di Milano.
- Strisce blu, poi strisce bianche libere.
- Piano marketing e ASO (IT/EN) attivo.
- Monitoraggio costante di calibrazione e segnalazioni.

**Metriche di uscita:**
- Rating store ≥ 4.0 (obiettivo da confermare).
- Calibrazione entro la tolleranza definita in `01-visione-e-scope.md`.
- Nessun incidente privacy aperto.

## Iterazione 4 — Prodotto completo
**Obiettivo:** prodotto maturo per Milano, con basi per altre città.

- Parcheggi di struttura e garage con disponibilità.
- Previsione all'orario di arrivo (ETA), con affidabilità esplicita.
- Tariffe e orari integrati.
- Eventuali partnership per il pagamento (EasyPark, Telepass, MooneyGo, ecc., da valutare).
- Architettura pronta per altre città (decisione separata).

## Regole di passaggio tra iterazioni

Un'iterazione è chiusa solo se:
1. tutte le metriche di uscita sono raggiunte o il fallimento è documentato;
2. `privacy-compliance` ha approvato il rilascio;
3. il `competitor-analyst` ha aggiornato `02-concorrenza.md`;
4. il fondatore ha confermato il passaggio.
