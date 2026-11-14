# 03 — Privacy e protezione dei dati

Stato: **principi di progetto**. Non sostituiscono un parere legale. Prima del lancio pubblico serve: DPIA (valutazione d'impatto), privacy policy firmata dal fondatore, e revisione di un professionista privacy/legale.

## Principi

1. **Minimizzazione.** Raccogliamo solo ciò che serve a stimare la disponibilità di posti. Non serve sapere chi guida né dove va.
2. **Elaborazione sul dispositivo.** Dove possibile, il rilevamento "ho parcheggiato / ho lasciato il posto" avviene sul telefono. Il server riceve solo l'evento, non la traccia GPS.
3. **Nessuna traccia grezza sul server.** Le posizioni GPS continue non vengono mai salvate lato server.
4. **Aggregazione.** Il dato pubblicato è per cella geografica (es. esagono H3) e per fascia oraria. Una cella viene mostrata solo se ci sono almeno **k contributi distinti** (proposta: k = 5). Questo protegge da re-identificazione.
5. **Identificatore pseudonimo.** Ogni installazione ha un ID casuale, ruotato periodicamente. Nessun nome, email o numero di telefono è richiesto per usare l'app di base.
6. **Consenso esplicito e separato.** Il consenso alla localizzazione è chiesto con una spiegazione chiara, separato dalle notifiche e revocabile in qualsiasi momento.
7. **Localizzazione in background solo se serve e solo se attivata dall'utente.** La modalità di rilevamento automatico è opzionale. Senza di essa, l'app funziona con segnalazioni manuali.
8. **Retention.** Eventi grezzi: massimo 30 giorni, poi aggregati e cancellati. Dati aggregati: conservati per il tempo necessario al modello, senza riferimenti all'utente.
9. **Diritti dell'utente.** Accesso, correzione, cancellazione, revoca del consenso, portabilità. Ogni diritto deve essere esercitabile dall'app in massimo 3 tap.
10. **Nessun tracking pubblicitario.** Niente SDK pubblicitari o di profilazione in v1. Le analytics, se presenti, sono aggregate e senza identificatori esterni.
11. **Dati in UE.** Hosting e database in regione europea. Elenco dei sub-responsabili documentato e aggiornato.
12. **Nessun video.** Non si raccolgono immagini, video o dashcam. (Questo ci distingue da SpotAngels.)

## Cosa raccogliamo (v1)

| Dato | Dove | Quanto | Base giuridica (da confermare) |
|---|---|---|---|
| ID pseudonimo | Dispositivo + server | Fino a revoca | Consenso / esecuzione del servizio |
| Evento "ho parcheggiato" / "ho lasciato" | Dispositivo → server | 30 giorni grezzi, poi aggregato | Consenso |
| Segnalazione manuale ("non c'era posto") | Dispositivo → server | Come sopra | Consenso |
| Posizione (anonimizzata a cella) | Dispositivo → server | Come sopra | Consenso |
| Lingua, piattaforma, versione app | Dispositivo → server | Aggregato | Interesse legittimo (da valutare) |

**Non raccogliamo:** traccia GPS continua, contatti, dati di pagamento, immagini, dati di salute, dati di minori.

## Vincoli tecnici (v2)

Rivisti da `privacy-compliance` il 2026-11-14 (T-018, T-028). Motivi e condizioni C1–C12 → [`15-dpia-bozza.md`](15-dpia-bozza.md) (bozza non firmata). Ogni voce è marcata confermato, corretto o nuovo.

- [confermato] **Riduzione sul dispositivo:** la posizione diventa cella H3 e l'orario è arrotondato alla fascia **prima** dell'invio. Il server non riceve mai coordinate.
- [confermato] **La mappa non rivela dove guarda l'utente:** l'app scarica la griglia intera di Milano come file statico. Nessuna richiesta contiene posizione o destinazione.
- [corretto] **Soglia k = 5 pseudonimi distinti** per cella, fascia e tipo, nella finestra "adesso" e nello storico; sotto soglia solo il prior. **k non si abbassa in beta** (si allargano celle e fasce, T-029). (C2)
- [corretto] **Rilevamento automatico** (D-018): **veto sulla forma attuale di D-018**; ammesso in beta chiusa solo con C1–C12, decisione scritta del fondatore e DPIA firmata. Innesco Bluetooth + attività "in auto", GPS solo nella fase di ricerca, notifica visibile; percorso solo in memoria. Al server solo sosta (con scaglione) e ripartenza: niente "inizio ricerca", niente durata della sosta. (C3–C5)
- [corretto] **Pubblicazione a intervalli fissi** (5 minuti, D-019): da sola **non** impedisce il confronto tra versioni. Una cella si aggiorna solo con ≥ 2 nuovi pseudonimi; probabilità in classi, affidabilità in 3 livelli, mai conteggi. (C6)
- [nuovo] **Invio ritardato** 0–10 min a caso; il server scarta l'ora di arrivo. (C7)
- [corretto] **Identificatore:** non più un ID unico a rotazione 24h (lega le soste di un giorno), ma uno **pseudonimo per cella** `HMAC(segreto, tipo‖cella‖epoca 28 gg)`, con segreto solo sul telefono. Sosta e ripartenza non collegabili. (C1)
- [corretto] **Diritti:** il telefono tiene il registro locale dei propri contributi e ricalcola gli pseudonimi per accesso e cancellazione; dopo 30 giorni restano solo aggregati senza pseudonimi. (C10)
- [nuovo] **Zone escluse proposte in automatico** (notte, orari di lavoro, calcolo locale) e **massimo 1 evento per tipo e cella al giorno**. (C8, C9)
- [nuovo] **Nessun backup cloud** di coordinate, zone escluse, segreto e registro. (C11)
- [nuovo] **Informativa ai tester:** chi li conosce potrebbe dedurne la presenza in una zona; T3 non è condizione per la beta. (C12)
- [corretto] **Log** senza indirizzi IP, posizione né ora esatta, anche presso il fornitore (vincolo per T-030); verificati da test automatico.
- [confermato] **Senza consenso** l'app resta utilizzabile: mappa e regole di sosta.
- [confermato] **Funzioni solo sul dispositivo** ("ricorda dove ho parcheggiato", timer, contatore dei contributi): nessun dato lascia il telefono.
- [confermato] **Segnalazione dei crash** solo con consenso e senza posizione.
- [corretto] **Test di re-identificazione** (`make reid`) prima di ogni build distribuita: specifica in [`15-dpia-bozza.md` §9](15-dpia-bozza.md#9-test-di-re-identificazione-prima-di-ogni-release). Se un attacco riesce, la release è bloccata.
- Antiabuso e piano incidenti → [`12-sicurezza.md`](12-sicurezza.md).

- **Veicolo (D-023):** il modello resta sul telefono; l'invio della taglia con i contributi è **in attesa di parere** (T-036). Nessun invio del tratto di strada senza parere (T-035).

## Requisiti store

→ [`10-release.md`](10-release.md) (fonte unica). Punto chiave: Apple richiede il consenso anche per dati anonimi.

## Checklist prima di ogni release

- [ ] Nuove raccolte di dati elencate in questo documento
- [ ] Consensi e revoca testati
- [ ] Privacy policy IT/EN aggiornata
- [ ] Etichette store aggiornate
- [ ] Nessuna chiave o credenziale nel codice
- [ ] Log senza dati personali
- [ ] Retention e cancellazione verificate con test
- [ ] Test di re-identificazione superato
- [ ] Nessuna coordinata o indirizzo IP nelle richieste e nei log

## Processo

`privacy-compliance` ha **potere di veto** su qualsiasi task che aumenti la raccolta di dati. Il veto si registra in `TASKS.md` e viene discusso con il fondatore prima di procedere.
