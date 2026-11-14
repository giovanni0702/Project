# 12 — Sicurezza

Stato: **bozza di progetto**, da completare in T-019 prima di esporre qualsiasi API. Vincoli privacy: [`03-privacy.md`](03-privacy.md).

## 1. Cosa proteggiamo

1. L'anonimato dei contributori (nessun evento riconducibile a una persona).
2. L'integrità delle stime (nessuno deve poterle falsare).
3. La disponibilità della griglia pubblicata.
4. Segreti e chiavi di servizio.

## 2. Minacce e contromisure

| Minaccia | Contromisura | Stato |
|---|---|---|
| Segnalazioni false in massa per alterare una zona | Limite di frequenza per identificatore e per rete; peso massimo per contributore; controlli di plausibilità (velocità, distanza, orario) | Da fare |
| Client non autentici (script) | Attestazione del dispositivo (App Attest / Play Integrity) **solo dopo parere di `privacy-compliance`** | Da valutare |
| Isolare un contributore confrontando due pubblicazioni | Pubblicazione a intervalli fissi; soglia k; test di re-identificazione prima di ogni release | Da fare |
| Posizione dedotta dalle richieste | L'app scarica la griglia intera; nessuna richiesta contiene posizione o destinazione | Decisa (D-011) |
| Indirizzi IP o posizioni nei log | Log applicativi senza IP e senza celle per evento; test automatico | Da fare |
| Segreti nel repository | `scripts/check_secrets.py` in `make check` e in CI; `.env` escluso da git | Attiva |
| Dipendenze vulnerabili | Scansione in CI; controllo a ogni ciclo di `ops-watchdog` | Dall'iterazione 1 |
| Accesso al database | Rete privata, utente applicativo con privilegi minimi, backup cifrati in UE | Dall'iterazione 1 |

## 3. Regole per le API

- Solo HTTPS. Convalida rigida degli ingressi dal contratto OpenAPI; campi sconosciuti rifiutati.
- L'API di scrittura accetta solo: tipo di evento, cella H3, fascia oraria, identificatore a rotazione, versione dell'app.
- Nessun endpoint restituisce eventi singoli. In lettura esiste solo la griglia aggregata.
- Interruttore remoto per sospendere la raccolta senza una nuova release.

## 4. Piano per incidenti

1. **Contenere:** sospendere raccolta o pubblicazione con l'interruttore remoto.
2. **Valutare:** quali dati, quante persone, per quanto tempo. Scrivere i fatti in un file datato.
3. **Avvisare il fondatore subito.** In caso di violazione di dati personali il GDPR prevede la notifica al Garante entro 72 ore: decide e firma il fondatore, `privacy-compliance` prepara la bozza.
4. **Correggere e verificare**, poi aprire un task con la causa e la prevenzione.

Nessun agente comunica all'esterno un incidente.
