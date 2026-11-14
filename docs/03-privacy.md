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

Proposti il 2026-11-14, da confermare da `privacy-compliance` in T-018 prima di scrivere codice di raccolta.

- **Riduzione sul dispositivo:** la posizione diventa cella H3 e l'orario è arrotondato alla fascia **prima** dell'invio. Il server non riceve mai coordinate.
- **La mappa non rivela dove guarda l'utente:** l'app scarica la griglia intera di Milano come file statico. Nessuna richiesta contiene posizione o destinazione.
- **Sotto soglia k** la cella mostra solo il prior, con affidabilità bassa. La soglia vale per gli aggregati derivati dagli utenti.
- **Rilevamento automatico tramite posizione** (D-018): solo dopo DPIA firmata; percorso mai inviato e cancellato sul telefono; al server solo evento, cella, fascia e tempo di ricerca a scaglioni; zone escluse; spento in partenza.
- **Pubblicazione a intervalli fissi** (ogni 5 minuti, D-019), per impedire di isolare un contributo confrontando due versioni.
- **Rotazione dell'identificatore** (proposta: ogni 24 ore). Gli eventi "ho parcheggiato" e "ho lasciato" non sono collegati tra loro sul server.
- **Diritti e rotazione:** accesso e cancellazione valgono per gli identificatori ancora sul dispositivo; dopo la rotazione il dato non è più riconducibile. Scelta da motivare nella DPIA.
- **Log** senza indirizzi IP e senza posizione, verificati da test automatico.
- **Senza consenso** l'app resta utilizzabile: mappa e regole di sosta.
- **Funzioni solo sul dispositivo** ("ricorda dove ho parcheggiato", timer, contatore dei contributi): nessun dato lascia il telefono.
- **Segnalazione dei crash** solo con consenso e senza posizione.
- **Test di re-identificazione** prima di ogni release: uno script tenta di isolare singoli contributori dagli aggregati. Se riesce, la release è bloccata.
- Antiabuso e piano incidenti → [`12-sicurezza.md`](12-sicurezza.md).

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
