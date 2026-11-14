# 01 — Visione e scope

## Problema
Cercare parcheggio in città è una perdita di tempo, carburante e stress. Oggi gli automobilisti non sanno in anticipo se in una via c'è posto. Le app esistenti mostrano dove si può parcheggiare o come pagare, ma stimano poco la probabilità di trovare un posto libero al momento dell'arrivo.

## Prodotto
Un'app che risponde a una domanda: **"Se vado lì adesso, quante probabilità ho di trovare posto entro 5 minuti?"**

- Mappa della città con zone colorate: verde (alta probabilità), giallo (media), rosso (bassa), grigio (dati insufficienti).
- Ogni zona mostra la probabilità e un indicatore di affidabilità ("basata su dati recenti" / "stima storica").
- Previsione per orario di arrivo: "alle 18:30 in via X la probabilità è del 40%".
- Un tap per avviare la navigazione verso la zona scelta (Google Maps o Waze).
- Contributo semplice degli utenti: "ho lasciato il posto", "non c'era posto". Sono il dato più prezioso.

## Utente target (v1)
- Automobilisti che si spostano in centro a Milano per lavoro, shopping o visite.
- Residenti che cercano posto sotto casa (priorità da valutare in iterazione 2).
- Non è un prodotto per flotte o aziende in v1.

## Scope del pilota
- **Area:** intero territorio del Comune di Milano. Si parte da una griglia della città, con la copertura più fitta dove il traffico e la domanda sono maggiori.
- **Tipologia di posto:** prima strisce blu (sosta regolamentata a pagamento), poi strisce bianche libere, poi parcheggi di struttura.
- **Lingue:** italiano e inglese dal lancio.
- **Piattaforme:** iOS e Android con un'unica codebase.

Fuori scope fino a decisione esplicita: Roma, altre città, flotte, pagamenti integrati, prenotazioni.

## Successo del pilota (indicatori)
- Calibrazione: su osservazioni reali, le probabilità previste corrispondono agli esiti reali entro una tolleranza da definire (es. ±10 punti percentuali).
- Copertura: percentuale di strade della città con una stima non "grigia".
- Attivazione: utenti che tornano nella stessa settimana.
- Contributi: segnalazioni per utente attivo a settimana.

## Vincoli
- Un solo fondatore, più agenti AI. Velocità a iterazioni, non a big bang.
- Budget da definire. Preferire servizi con piani gratuiti o economici.
- GDPR come requisito di base, non come aggiunta finale.
- Nessun dato di terze parti usato in violazione dei loro termini.
