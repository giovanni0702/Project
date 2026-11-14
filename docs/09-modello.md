# 09 — Modello probabilistico

Stato: **progetto, nessun dato reale ancora**. Nessuna accuratezza è dichiarata. Parametri numerici in `model/config/` (dall'iterazione 1), non qui.

## 1. Bersaglio

**Y = 1** se una ricerca di parcheggio iniziata nella cella *c*, nella fascia *s*, trova posto **entro 5 minuti**. Il modello stima P(Y = 1 | c, s).
Senza un Y osservabile non esiste calibrazione: ogni fonte di dati deve produrre un esito sì/no.

## 2. Come si osserva Y

| Fonte | Esito | Uso | Quando |
|---|---|---|---|
| Contributo manuale a un tap: "trovato subito" / "trovato dopo un po'" / "non trovato" | Y diretto | Addestramento | Iterazione 2 |
| Rilevamento automatico sul dispositivo, tramite posizione e Bluetooth dell'auto (D-018): tempo di ricerca misurato | **Y diretto** (tempo ≤ 5 minuti) | Addestramento | Solo dopo DPIA (T-028) |
| Quota di esiti dei tester tenuta da parte, più "missioni" di copertura (T-021, D-015) | Y diretto | **Solo validazione**, mai addestramento | Iterazione 2 |

Non sono previste rilevazioni sul campo: **fino alla beta il prior non è validato** e si mostra sempre con affidabilità bassa.

Gli eventi "ho parcheggiato" e "ho lasciato" senza esito di ricerca alimentano solo il modello a tassi (§3.3).

## 3. Scala dei modelli

Un modello si adotta solo se batte il precedente **su dati reali**, con intervallo di confidenza.

1. **Baseline (obbligatorio):** frequenza di successo per cella e fascia; sotto la soglia minima di osservazioni, frequenza di zona.
2. **Beta-Binomiale gerarchico:** prior Beta per cella e fascia derivato dai proxy (§4); aggiornamento con gli esiti; shrinkage verso zona, città e celle vicine; decadimento esponenziale degli esiti vecchi (emivita da validare).
3. **Modello a tassi:** λ = posti liberati al minuto, prior Gamma(α, β), aggiornamento α += eventi, β += tempo osservato. La forma semplice P(t) = 1 − e^(−λt) **non è adottabile da sola**, per due motivi:
   - **concorrenza:** un posto liberato è conteso da altri automobilisti in cerca; serve il tasso di domanda μ;
   - **penetrazione:** gli eventi osservati sono una frazione ignota di quelli reali; senza stimarla λ è sottostimato.

In iterazione 1 si costruiscono 1 e 2. Il modello 3 è un task di ricerca, non un impegno.

### Componente "adesso" e miglioramento automatico (D-018, D-019)
- La griglia si ricalcola ogni 5 minuti. Gli esiti recenti (finestra e peso in configurazione) contano di più e valgono per la fascia corrente.
- Emivita, peso dei dati recenti e soglie si ricalibrano periodicamente su dati reali tenuti da parte, mai a mano e mai su dati sintetici (T-032).

### Strade, orari, veicolo (D-021, D-022, D-023)
- **Strade:** la stima si calcola per cella; ogni tratto di strada la eredita, corretta dalle sue caratteristiche fisse (stalli, tipo di sosta, regole). Non è una misura live del singolo tratto.
- **Altri orari e giorni:** solo la componente storica per fascia e tipo di giorno, mostrata come stima.
- **Veicolo:** correzione per taglia applicata sul telefono, stimata a livello di città. Valori iniziali non validati. Le moto richiedono dati e modello propri.

## 4. Variabili

- **Tempo:** fascia di 30 minuti × tipo di giorno (feriale, sabato, festivo); festività; calendario scolastico.
- **Regole:** orari e tariffe della sosta, Area C, ambiti residenti, lavaggio strade, mercati.
- **Contesto:** densità di uffici, scuole, stazioni, negozi (OSM, ISTAT); eventi; scioperi; meteo.

Fonti e licenze: [`06-dati.md`](06-dati.md). Una variabile entra solo se la fonte è verificata e la licenza lo permette.

## 5. Distorsioni note

| Distorsione | Mitigazione |
|---|---|
| Chi non trova posto segnala con frequenza diversa da chi lo trova | Missioni di copertura assegnate ai tester (zone e orari scelti da noi, non da loro); correzione stimata e documentata |
| I contributori non sono un campione degli automobilisti | Dichiarato nei limiti; nessuna estrapolazione a zone senza dati |
| Pochi contributori dominano una cella | Peso massimo per contributore per cella e fascia |
| Segnalazioni false o automatiche | Controlli di plausibilità → [`12-sicurezza.md`](12-sicurezza.md) |

## 6. Metriche

- **Calibrazione:** diagramma di affidabilità ed errore medio; tolleranza proposta ±10 punti.
- **Brier score** e **miglioramento percentuale sul baseline**.
- **Copertura:** quota di celle non grigie. **Nitidezza:** quanto le stime si allontanano dalla media.
- Sempre con intervallo di confidenza e numero di osservazioni. Sotto l'N minimo (da fissare in T-010) non si dichiara nulla.
- **Validazione temporale:** si addestra sul passato, si valuta sul futuro. Mai divisione casuale.
- **Deriva:** le metriche si ricalcolano a ogni pubblicazione; un peggioramento oltre soglia apre un task.

## 7. Dal numero allo schermo

- **Affidabilità a tre livelli** (alta / media / bassa), funzione del numero di esiti e dell'età dell'ultimo.
- **Colori:** soglie fissate sulle probabilità calibrate. Isteresi: una zona cambia colore solo se supera la soglia con margine.
- **Grigio:** nessuna stima difendibile. Sotto k contributori (→ [`03-privacy.md`](03-privacy.md)) si mostra solo il prior, con affidabilità bassa.
- **Priorità centro:** raccolta e calibrazione partono dal centro; il resto del Comune riceve il prior.

## 8. Regole sui dati

- Dati sintetici: sempre etichettati, in cartelle separate, mai mescolati ai reali. Ogni report sintetico dichiara: *"test tecnico, non misura di accuratezza"*.
- Riproducibilità: seed, versione dei dati e parametri in file di configurazione; un comando rigenera tutto.

## 9. Scheda del modello (limiti e usi non previsti)

- Stima una probabilità per zona e fascia, non la presenza di un posto specifico.
- Non è una garanzia e non sostituisce la segnaletica: le regole di sosta valgono sempre.
- Non usare per sanzioni, controllo della sosta o profilazione di persone.
- Fuori da Milano il modello non è valido.
