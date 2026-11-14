# 18 — Nota informativa per i tester (beta)

**BOZZA — richiede revisione di un professionista e approvazione del fondatore.** Non è un parere legale. I punti tra parentesi quadre vanno completati. Riferimenti normativi **[verificare]**: GDPR artt. 13, 6, 7, 15–21 non ancora letti alla fonte (vedi [`15-dpia-bozza.md`](15-dpia-bozza.md) §12).

## Chi siamo
Titolare del trattamento: [TITOLARE] (persona fisica). Contatto: [EMAIL]. Nessun responsabile della protezione dei dati nominato **[verificare]**.

## A cosa serve
L'app stima la probabilità di trovare parcheggio in strada a Milano. I tuoi contributi servono solo a questo: nessuna pubblicità, nessuna profilazione, nessuna vendita.

## Cosa raccogliamo
- **Tap manuale** (se acconsenti): cella della mappa (un'area di circa un isolato), fascia di 30 minuti, esito, un codice casuale.
- **Rilevamento automatico** (**spento in partenza**, consenso separato): tipo di evento (sosta o ripartenza), cella, fascia, tempo di ricerca a scaglioni (0–2, 2–5, 5–10, oltre 10 minuti), codice casuale. Per funzionare usa la posizione **anche quando l'app è chiusa** e il Bluetooth della tua auto.
- Il codice casuale è calcolato sul telefono e cambia da una cella all'altra: il server non può collegare i tuoi eventi in celle diverse.

## Cosa NON raccogliamo
Coordinate precise, percorso, ora esatta, durata della sosta, indirizzo IP nei registri dell'app, nome o indirizzo Bluetooth dell'auto, contatti, identificativi pubblicitari. "Ricorda dove ho parcheggiato" resta solo sul telefono. Nessun backup su cloud di questi dati.

## Base giuridica
Il tuo **consenso** (art. 6(1)(a) GDPR **[verificare]**), separato per tap manuale e rilevamento automatico. Partecipare al rilevamento automatico non è condizione per la beta. Per l'accesso a posizione e Bluetooth del telefono vale anche l'art. 122 Codice privacy **[verificare]**.

## Conservazione
I dati grezzi restano sul server **30 giorni**, poi restano solo aggregati senza codici. Il percorso resta in memoria sul telefono e viene cancellato appena prodotto l'evento.

## I tuoi diritti
Puoi chiedere accesso, cancellazione, limitazione e opposizione e revocare il consenso in ogni momento (**[verificare]** artt. 7(3), 15–21 GDPR). Dall'app: registro dei tuoi contributi, revoca in al massimo 3 tap, cancellazione dei tuoi dati (il telefono ricalcola i codici e li invia). **Se disinstalli l'app il segreto che genera i codici viene cancellato**: dopo non potremo più ritrovare i tuoi dati, che spariscono comunque entro 30 giorni. Puoi anche scrivere a [EMAIL]. Hai diritto di reclamo al Garante per la protezione dei dati personali.

## Un avviso onesto
Siamo in pochi e forse ci conosciamo. Chi ti conosce potrebbe dedurre che eri in una certa zona vedendo la mappa cambiare. Per questo la mappa mostra solo classi, mai conteggi, e una cella si aggiorna solo con almeno 2 contributi nuovi. Se non ti va bene, usa solo il tap manuale o niente.

## Uso dei dati
Solo per la beta, in UE [hosting da scegliere, T-030]. Nessun SDK di terze parti per analisi o pubblicità. Nessun dato Google usato nel modello.

## Revisione
Versione [N] del [DATA]. Approvata dal fondatore: ______ · Revisione professionale: ______
