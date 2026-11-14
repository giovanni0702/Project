# 11 — Marketing

Stato: **BOZZE — non pubblicare, non inviare, non contattare senza approvazione del fondatore.** Versione 2026-11-14, per la beta Android su tutto il Comune (D-017, D-029). Base: [`02-concorrenza.md`](02-concorrenza.md) §4, [`16-grafica.md`](16-grafica.md), [`05-decisioni.md`](05-decisioni.md).

Regole: nessuna cifra di accuratezza in alcun testo finché `data-scientist` non l'ha misurata (`09-modello.md`). Ogni testo esiste in italiano e in inglese. Il reclutamento non parte prima che la correzione del red team (T-040) sia chiusa e la build approvata (`STATO.md`).

## 1. Posizionamento

- **Frase (IT):** Sai dove parcheggiare a Milano prima di partire.
- **Frase (EN):** Know where to park in Milan before you leave.
- **Per chi:** chi guida o va in moto a Milano e perde tempo a cercare posto in strada.

### Tre messaggi chiave

1. **Vedi prima di partire.** Ogni strada ha un colore: facile, possibile, difficile. Accanto al colore è sempre scritto il livello.
   - EN: Every street has a colour: easy, maybe, hard. The level is always written next to it.
2. **Dati degli utenti, anonimi.** Un tocco quando trovi o non trovi posto. Niente nome, niente account, niente video.
   - EN: One tap when you find a spot, or don't. No name, no account, no video.
3. **Ti diciamo quanto è affidabile il dato.** Il dettaglio di strada cresce con i contributi. Dove non sappiamo, lo scriviamo.
   - EN: The street detail grows with contributions. Where we don't know, we say so.
   - Nota: il messaggio "tutta la città ha un dato fin da subito" dipende da T-045 (stima a livelli). Finché non è attiva, non va usato.

### Non promettiamo
Un posto garantito. Una percentuale di precisione. Dati in tempo reale dove non ci sono contributi. Tariffe o orari che non abbiamo verificato.

### Tono
Diretto, concreto, mai allarmistico. Niente gergo statistico: nella scheda si dice "7 volte su 10", mai "probabilità calibrata".

## 2. Nomi proposti

Scelta del fondatore (cambio di nome = decisione riservata, CLAUDE.md §7). **Tutti i nomi: marchio da verificare.** Nessuna ricerca marchi è stata eseguita: va fatta su UIBM ed EUIPO prima di usarne uno.

| # | Nome | Pronuncia IT / EN | Pro | Contro |
|---|---|---|---|---|
| 1 | **Milosta** | mi-LO-sta / mi-LO-sta | Milano + sosta: locale, memorabile, unico | Parola inventata: va spiegata una volta |
| 2 | **Sosta** | SO-sta / SO-sta | Breve, italiano, dice il gesto | Generico: marchi simili probabili; in EN poco chiaro |
| 3 | **Curbly** | — / KUR-bli | "Curb" = bordo del marciapiede; breve, EN friendly | Non italiano; nome già usato da altri (da verificare) |
| 4 | Postomi | POS-to-mi / POS-to-mi | Suona come "trova un posto per me" | Può sembrare dialettale |
| 5 | Stallo | STAL-lo / STAL-lo | "Stallo" = posto auto in gergo | In italiano vuol dire anche blocco |
| 6 | Spotwise | — / SPOT-waiz | "Spot" = posto, "wise" = sapere | Inglese in città italiana; "spot" molto usato |
| 7 | Dove Sosto | DO-ve SO-sto | Promessa nel nome | Lungo; a voce non si scrive |
| 8 | Trovaposto | tro-va-POS-to | Descrive la funzione | Lungo; generico |
| 9 | Ciao Posto | CIA-o POS-to | Caldo, italiano, facile da ricordare | Non dice che è un parcheggio |
| 10 | Strada Facile | — | Promessa semplice | "Facile" è una promessa che non possiamo garantire |

Raccomandazione: **Milosta** per il ricordo, con sottotitolo "Parcheggio a Milano" per la chiarezza; **Sosta** come alternativa se si preferisce un nome comune; **Curbly** solo per una versione internazionale futura. Opzioni scartate: nomi con "sicuro", "garantito" o "facile" nel nome.

## 3. Ganci di prodotto (senza dati personali)

Principi: ogni gancio usa solo dati aggregati o dati che restano sul telefono. Nessun gancio mostra dove, quando o quanto ha sostato una persona. Nessun profilo pubblico, nessuna classifica di persone, nessun codice di invito personale.

| # | Gancio | Cosa vede l'utente | Beneficio atteso | Sforzo | Rischio privacy (da far valutare a `privacy-compliance`) |
|---|---|---|---|---|---|
| G1 | Scheda da condividere, generata sul telefono | "Oggi in Isola: 7 strade su 10 facili" (dato di zona, non della persona) | Alto: è il passaparola | Basso: immagine locale, nessun server | Basso se mostra solo livello quartiere o città. Alto se mostra "parcheggiato in 2 minuti alle 18:40": dato personale su luogo e ora, rivelabile in zone piccole. **Si fa solo la versione "dato di zona".** |
| G2 | Contatore locale | "Hai aiutato 14 volte" | Medio: ritorno all'app | Basso | Basso: il dato non esce dal telefono. Non deve finire nei log. |
| G3 | Missioni di quartiere | "In Isola mancano dati su 3 strade: segnalane una" | Alto per la copertura (D-029) | Medio: regole lato server su conteggi aggregati | Medio: pressione a contribuire; una missione mirata su zone piccole può rivelare presenza. Solo sopra soglia, mai missioni personali. |
| G4 | Classifica dei quartieri | "Municipi con i dati più recenti" | Medio: senso di gara tra zone | Basso | Medio: zone con pochi contributori sono deducibili. Solo sopra soglia, a livello di Municipio (9). Attivare dopo il red team. |
| G5 | Invito con link semplice | Link diretto alla pagina di download | Alto: passaparola | Minimo | Basso, a patto che la pagina non registri IP in chiaro (§5). Niente parametri, niente link accorciati con statistiche. |
| G6 | "La tua Milano" | Riepilogo sul telefono: strade viste, tuoi orari, consiglio per domani | Alto per la fidelizzazione | Medio | Basso-medio: resta sul telefono, va spiegato nell'informativa e deve poter essere cancellato. |

Non si usano: sfide tra amici con nomi (richiedono identità); premi in denaro o buoni (spesa, D-014); pubblicità; il rilevamento automatico come argomento di marketing (D-018: attivo solo dopo DPIA, spento di default).

## 4. Piano di reclutamento: 4 settimane, costo zero

**Settimana 0 (gate, nessun invito).** Chiudere T-040 e la build. Preparare: pagina di presentazione (sotto), nota per i tester (`18-nota-tester.md`), installazione provata su 2 telefoni da `qa-tester` (T-043). Ogni messaggio è una bozza in attesa del fondatore.

| Settimana | Installazioni cumulative (ipotesi) | Contributi nella settimana (ipotesi) | Canali |
|---|---|---|---|
| 1 | 25 | 20 | Cerchia di fiducia del fondatore |
| 2 | 100 | 100 | Gruppi di quartiere, motociclisti, università |
| 3 | 250 | 300 | Pendolari, uffici del centro |
| 4 | 500 | 600 | Passaparola con scheda G1 e invito G5 |

Gli obiettivi si rivedono dopo la settimana 1. Le installazioni non si misurano senza identificativi: vedi §5.

### Messaggi per canale (bozze)

**Canale 1 — cerchia (sett. 1).** Destinatari: persone che il fondatore conosce già.
- IT: "Ciao, sto provando un'app per capire dove parcheggiare a Milano. Ti chiedo 10 minuti per installarla e dirmi cosa non è chiaro. Non serve nessun account. File e passaggi: [link]."
- EN: "Hi, I'm testing a small app that shows where to park in Milan. Could you install it and tell me what's unclear? About 10 minutes, no account needed: [link]."

**Canale 2 — gruppi di quartiere (sett. 2).**
- IT: "Ho fatto un'app per Milano che mostra strada per strada quanto è facile parcheggiare. I dati arrivano da noi, in modo anonimo, con un tocco. È in beta e gratuita. Se la provate, ditemi quale strada del vostro quartiere non torna."
- EN: "I built an app for Milan that shows, street by street, how easy parking is. The data comes from us, anonymously, one tap at a time. It's a free beta. If you try it, tell me which street in your area doesn't add up."

**Canale 3 — motociclisti (sett. 2).** Il dato per le moto è ancora incompleto (`STATO.md`): il messaggio chiede un riscontro, non promette.
- IT: "Stiamo testando un'app per Milano con la scelta del veicolo, anche la moto. Scegli 'moto' e dicci se le stime ti sembrano giuste e dove mancano."
- EN: "We're testing a Milan app with a vehicle choice, motorbikes included. Pick 'motorbike' and tell us if the estimates look right and where they're missing."

**Canale 4 — università (sett. 2).** Il contatto passa da associazioni studentesche, solo con decisione del fondatore.
- IT: "Chi arriva in auto o in moto in università? Cerchiamo 20 volontari per 2 settimane di prova. Nessun account, un sondaggio di 5 domande anonimo alla fine."
- EN: "Do you drive or ride to campus? We're looking for 20 volunteers for two weeks of testing. No account, and a 5-question anonymous survey at the end."

**Canale 5 — pendolari (sett. 3).**
- IT: "Se ogni giorno cerchi posto in auto a Milano, prova l'app per due settimane e dimmi in quale strada ti è costato più tempo."
- EN: "If you look for a spot in Milan every day, try the app for two weeks and tell me which street cost you the most time."

**Canale 6 — uffici del centro (sett. 3).** Bozza per il fondatore: nessun invio senza sua decisione.
- IT: "Gentile team, stiamo testando un'app per chi arriva in auto a Milano. Mostra quanto è facile parcheggiare strada per strada, senza account né pubblicità. Se vi interessa, possiamo inviarvi il file di prova e la nota sulla privacy."
- EN: "Hello team, we're testing an app for people who drive into Milan. It shows how easy parking is street by street, with no account and no ads. If you're interested, we can send you the test file and the privacy note."

**Canale 7 — passaparola (sett. 4).**
- IT: "Ti passo un'app per trovare posto a Milano, senza dare dati e senza annunci: [link]. Provala e dimmi se ti torna."
- EN: "Here's an app for finding parking in Milan, with no data sharing and no ads: [link]. Try it and tell me if it works for you."

### Pagina di presentazione (bozza)

- **IT**
  - Titolo: *[Nome] — sai dove parcheggiare prima di partire.*
  - Ogni strada di Milano ha un colore: facile, possibile, difficile. Accanto al colore c'è sempre scritto il livello e quanto è affidabile il dato.
  - I dati arrivano dai tester: un tocco quando trovi o non trovi posto. Anonimo.
  - Nessun account. Nessun video. Nessuna pubblicità.
  - Se non abbiamo dati su una strada, lo diciamo.
  - Beta gratuita per Android. Come installarla: vedi sotto.
- **EN**
  - Title: *[Name] — know where to park before you leave.*
  - Every street in Milan has a colour: easy, maybe, hard. Next to the colour, we always show the level and how reliable the data is.
  - The data comes from testers: one tap when you find a spot, or don't. Anonymous.
  - No account. No video. No ads.
  - If we have no data for a street, we say so.
  - Free beta for Android. How to install it: see below.

### Installazione diretta, senza spaventare (bozza)

- **IT:** "L'app non arriva dal Play Store, quindi Android mostra un avviso standard per le app fuori dallo store. È normale in una beta. Per installarla: 1) apri il file; 2) se il telefono lo chiede, consenti l'installazione da questa fonte solo per questa app; 3) controlla che la scritta sia la stessa del file pubblicato. [Passaggi esatti da verificare su due telefoni: T-043.]"
- **EN:** "The app doesn't come from the Play Store, so Android shows a standard warning for apps installed outside the store. This is normal in a beta. To install: 1) open the file; 2) if your phone asks, allow installs from this source for this app only; 3) check that the checksum matches the one published on the page. [Exact steps to verify on two phones: T-043.]"
- Parole da evitare: "virus", "rischio", "pericoloso". Usare: "avviso standard", "beta".

## 5. Cosa misurare senza tracciamento

| Misura | Come | Dato | Vincolo |
|---|---|---|---|
| Contributi per giorno e per Municipio | Conteggi aggregati nel backend (cella H3 + fascia oraria) | Numero | Nessun identificativo. Soglia minima prima di mostrare il conteggio. |
| Installazioni | **Non misurabili senza identificativi.** Opzioni: A) contatore di download senza log IP (se il servizio lo permette); B) sondaggio volontario; C) stima dal passaparola | Numero | Scelta del fondatore con `privacy-compliance`. Raccomandazione: A, altrimenti C. |
| Tester attivi | Sondaggio volontario e anonimo, 5 domande, senza email né ID | Percentuale del campione | Testo approvato da `privacy-compliance`. |
| Chiarezza dell'installazione | Domanda nel sondaggio: "sei riuscito a installare senza aiuto?" | Sì/no | Stesso sondaggio. |

### Criteri per dire che il reclutamento funziona
- I contributi settimanali crescono per tre settimane di fila.
- Entro la settimana 4, almeno un contributo a settimana in almeno 5 dei 9 Municipi.
- Dal sondaggio: almeno 1 tester su 3 ha usato l'app più di una volta.

### Segnali di stop
- Dopo la settimana 2, meno di 20 contributi a settimana: si cambiano messaggi e canali, non si aggiungono funzioni.
- Più di 1 tester su 5 dice che l'avviso di Android lo ha fermato: si rivede la spiegazione dell'installazione prima di scalare.

## 6. Azioni solo del fondatore

1. Scegliere il nome (§2) e far fare la verifica dei marchi su UIBM ed EUIPO.
2. Scegliere il servizio per la pagina di download, con o senza log IP (T-030).
3. Approvare ogni messaggio (§4) e decidere ogni invio.
4. Inviare i messaggi a persone, gruppi, università e uffici: solo il fondatore.
5. Pubblicare la pagina di presentazione o caricare il file della beta.
6. Creare account su social, gruppi o canali, se servono.
7. Far approvare da `privacy-compliance` la nota per i tester (`18-nota-tester.md`) e il sondaggio.
8. Scegliere la versione di G1 (proposta: solo "dato di zona") e se attivare G6.
9. Decidere se attivare G3 (missioni) e G4 (classifica), dopo il red team.
10. Decidere, dopo la settimana 1, se proseguire, cambiare canali o rivedere gli obiettivi.
11. Decidere se contattare uffici o associazioni: contatti con enti (Comune, ATM) non sono previsti.
12. Approvare la chiusura e la cancellazione dei dati dei tester di prova (solo il fondatore, CLAUDE.md §7).
