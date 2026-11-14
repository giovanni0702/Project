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

Codice: `parking_core/metrics.py`; test tecnici (dati sintetici) in `tests/test_metrics.py`.

| Metrica | Definizione operativa | Funzione |
|---|---|---|
| Brier | media di (p − y)², y ∈ {0, 1}; più basso è meglio | `brier`, `brier_ci` |
| Miglioramento sul baseline | 1 − Brier_modello / Brier_baseline, sugli **stessi** esiti di validazione | `skill_vs_baseline` |
| Errore di calibrazione (ECE) | media pesata di \|p medio − frequenza osservata\| per classe di p; in beta **3 classi** = le classi pubblicate (bassa / media / alta) | `calibration_error(..., bins=3)`, `calibration_error_ci` |
| Diagramma di affidabilità | per classe: n, p medio, frequenza osservata | `reliability_table` |
| Copertura | quota di celle-fascia dell'area con dati utente pubblicabili (≥ k pseudonimi) | `scripts/beta_density.py` (simulazione) |
| Nitidezza | scarto medio delle stime dalla media di città | da fare (T-032) |

- **Tolleranza di calibrazione:** proposta ±10 punti (da confermare con il product-manager).
- **Intervallo di confidenza:** bootstrap percentile al 95%, 1000 ricampionamenti, seme fisso. Si ricampionano **contributori interi** (`groups`), non esiti singoli: gli esiti di una persona sono correlati e il bootstrap semplice darebbe intervalli troppo stretti.
- **N minimo (`enough_data`):** per una classe servono **97 esiti** perché l'intervallo al 95% della frequenza osservata stia entro ±10 punti (caso peggiore p = 0,5: 1,96² · 0,25 / 0,1²). Con 3 classi: **≥ 291 esiti di validazione** e **≥ 10 contributori distinti**. Sotto, non si dichiara nulla: né calibrazione né miglioramento sul baseline, nemmeno con intervallo. Con tolleranza ±5 punti servirebbero 385 esiti per classe.
- **Validazione temporale (`temporal_split`):** si addestra sul passato, si valuta sul futuro; mai divisione casuale. Gli esiti nell'intervallo `gap` prima del taglio si scartano, perché la componente "adesso" non trasmetta informazione oltre il confine. In beta si usa la forma **sequenziale**: ogni esito è previsto con il modello com'era prima di riceverlo, così tutti gli esiti servono alla validazione senza toglierli alla mappa.
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

## 10. Piano per la beta con pochi tester (T-029)

**Simulazione sintetica:** dimensiona la beta, non misura accuratezza. Comando: `.venv/bin/python scripts/beta_density.py` (seme 20261114, 20 ripetizioni, parametri da riga di comando). Ipotesi non verificate: profilo orario delle ricerche, abitudini (60% degli esiti liberi nei due luoghi abituali), 80% degli esiti liberi dentro l'area, 80% delle missioni eseguite, 10% di esiti riservati alla validazione, 4 settimane in una sola epoca di pseudonimi (C1). k = 5 pseudonimi distinti per cella, tipo di giorno e fascia, contati sulla **storia della fascia** (C2); al massimo un evento per persona, cella e giorno (C9).

| Tester × esiti/sett. | Area | Griglia | Fascia | Missioni | Copertura feriale ≥ k |
|---|---|---|---|---|---|
| 20 × 5 | 30 celle res 9 | res 9 | 30 min | 0% / 75% | **0% / 0%** |
| 100 × 5 | 30 celle res 9 | res 9 | 30 min | 0% / 75% | 1% / 0% |
| 20 × 5 | 30 celle res 9 | res 9 | 3 ore | 75% | 0% |
| 20 × 10 | 14 celle res 9 | res 9 | 3 ore | 75% | 92% |
| 20 × 5 | 30 celle res 9 (8 celle res 8) | res 8 | 3 ore | 0% / 75% | 26% / **85%** |
| 20 × 5 | 14 celle res 9 (4 celle res 8) | res 8 | 3 ore | 75% | **100%** |
| 20 × 5 | 14 celle res 9 | res 8 | 2 ore | 75% | 95% |
| 20 × 3 | 14 celle res 9 | res 8 | 3 ore | 75% | 97% |
| 10 × 5 | 14 celle res 9 | res 8 | 3 ore | 75% | 81% |
| 10 × 5 | 30 celle res 9 | res 8 | 3 ore | 75% | 10% |

Letture:
- **Con la configurazione attuale (res 9, 30 minuti) la mappa non mostra mai dati reali**, né con 20 né con 100 tester. Su Milano intera (circa 1.650 celle × 30 fasce diurne × 3 tipi di giorno ≈ 150.000 celle-fascia) 20 tester producono circa 400 esiti in 4 settimane: meno di uno ogni 300 celle-fascia.
- **"Stesso orario su più giorni" è indispensabile:** contando k nel singolo giorno nessuna configurazione con 20 tester supera k. Per lo stesso motivo la componente "adesso" non supera mai k in beta: si mostra solo la storia della fascia.
- **Le missioni contano più del numero di tester:** a parità di tutto, passare da 0% a 75% di missioni porta la copertura da 26% a 85%. Con fasce strette le missioni si disperdono e non aiutano.
- **Sabato e festivi restano grigi:** le missioni sono solo feriali; con 20 tester non bastano gli esiti spontanei.

**Raccomandazione per la beta (4 settimane):**
1. **Area:** 4 celle H3 res 8 contigue nel centro (circa 3 km², circa 28 celle res 9), scelte da noi.
2. **Unità di pubblicazione e di conteggio di k:** res 8 × blocchi di 3 ore (07–10, 10–13, 13–16, 16–19, 19–22) × giorno feriale = 20 celle-blocco. Il modello resta a res 9 / 30 minuti all'interno; la soglia si conta e la classe si pubblica sull'unità grossa.
3. **Minimo:** 20 tester attivi × 5 esiti a settimana, di cui 3–4 in missione. Con 10 tester serve un'area di 3 celle res 8 (95%) o 10 esiti a settimana a testa (99%). Sotto 10 tester attivi la mappa non mostra quasi nessun dato reale.
4. **Cosa vede il fondatore:** con il minimo, circa il 100% dei blocchi feriali delle 4 celle (simulato) ha dati reali, in classi e con affidabilità **bassa**; fuori area e nel fine settimana solo il prior.

**Missioni di copertura (zone e orari scelti da noi):** ogni tester riceve ogni settimana 3–4 coppie (cella res 8, blocco feriale), assegnate a rotazione in modo che ogni coppia abbia almeno 7 tester diversi nel ciclo (margine sopra k per chi salta la missione). L'app chiede solo l'esito a un tap quando il tester cerca parcheggio lì; nessun obbligo di spostarsi. Le missioni correggono anche la distorsione di segnalazione (§5).

**Quota di validazione:** (a) validazione **sequenziale** su tutti gli esiti (§6), senza toglierli alla mappa; (b) **10% degli esiti di missione**, estratti a caso dal server con seme registrato, mai usati per addestrare né per contare k: servono alla ricalibrazione di T-032. Con 20 × 5 per 4 settimane si raccolgono circa 280 esiti nell'area: **sotto l'N minimo (291)**. Dopo 4 settimane la beta dimostra che la mappa funziona, **non che le probabilità sono calibrate**; servono circa 5–6 settimane per la validazione sequenziale e alcuni mesi per la quota (b).

**Proposta di modifica a `cities/milano/city.yaml` (non applicata, decide il fondatore):**
```yaml
publish_unit:            # unit where k (C2) and C6 are counted and classes are published
  h3_resolution: 8       # model stays at grid.h3_resolution
  slot_minutes: 180
  day_types: [weekday]   # saturday/holiday: prior only during the beta
beta_area_res8: []       # 4 contiguous res-8 cells, chosen by us
validation_holdout: 0.10 # share of mission outcomes never used for training or k
```
Richiede codice in `parking_core/publish.py` e `privacy.py` (fuori da T-029) e revisione di `privacy-compliance`.

**Cosa non sappiamo ancora:** quanti esiti a settimana fa davvero un tester; quante missioni esegue; se una cella res 8 (lato circa 530 m) è abbastanza utile per chi cerca; il comportamento del fine settimana. **Rischio privacy da verificare:** lo pseudonimo cambia ogni 28 giorni (C1), quindi oltre un'epoca la stessa persona conta due volte per k; la beta deve stare in un'epoca o il conteggio va corretto.

> **Aggiornamento del 2026-11-14 (D-029):** il fondatore ha deciso che la beta copre tutto il Comune. La raccomandazione di concentrarla in un'area resta qui come analisi, ma non si applica: la via scelta è la stima a livelli (T-045).

## 11. Modello di occupazione (T-049)

> **Stato:** stime del modello da dati aperti e parametri dichiarati, **NON verificate**. Senza esiti reali nessun numero qui va presentato come misura. Niente dati Google (D-004).

**Codice:** `parking_core/occupancy.py` (solo libreria standard), `scripts/build_occupancy.py <città>` → `build/occupancy/<città>/occupancy.json`; parametri in `cities/milano/city.yaml` (`capacity:`, `occupancy:`); test in `tests/test_occupancy.py`.

**Formule** (per cella H3, tipo di giorno, fascia di 30 minuti):
- Capacità del marciapiede per tratto: `c = max(L − 2·arretramento, 0) · fattore_via · lati · quota_sostabile · (1 − quota_moto) / lunghezza_stallo`; più `(1 − sovrapposizione) ·` posti delle aree mappate (D-030). Stalli moto: `L_utile · lati · quota_sostabile · quota_moto / larghezza_stallo_moto`. Parcheggi in struttura esclusi (riportati a parte).
- Auto dei residenti in strada: `N = residenti_cella · auto_per_residente · quota_in_strada`. Residenti del quartiere (NIL) ripartiti sulle celle in proporzione alla lunghezza delle strade.
- Movimento: le partenze dei residenti e gli arrivi dei visitatori seguono il profilo a 30 minuti degli ingressi in Area C (forma 2016, totali per finestra e tipo di giorno 2023-24). Auto fuori casa e visitatori in sosta: carico offerto modificato `m(t+Δ) = m(t)·e^(−μΔ) + (λ/μ)(1 − e^(−μΔ))`, regime periodico.
- Visitatori: arrivi giornalieri per cella `= quota_in_strada_cordone · ingressi_cordone / attrattori_cordone · attrattori_cella · (moltiplicatore fuori cordone)`, con attrattori = unità locali + peso · residenti. Due classi di sosta (lavoro, breve).
- Carico offerto `a(t) = N·(1 − fuori_casa(t)) + visitatori(t)`; arrivi in cerca `λ(t) = rientri + arrivi visitatori`; `μ = λ/a` (Little).
- Erlang B con `c` reale: `B = pmf_Poisson(c; a) / Q(c+1, a)` (gamma incompleta regolarizzata, stabile per migliaia di posti). Erlang C: `C = B / (1 − ρ(1 − B))`, `ρ = a/c`.
- Attesa M/M/c: `P(W ≤ t) = 1 − C·e^(−(cμ − λ)t)`; se `λ ≥ cμ` non c'è regime: la funzione lo segnala e restituisce 0.
- **Sovraccarico, trattamento usato nel calcolo:** coda M/M/c/(c+K) a pazienza finita, `K = ⌈cμ·pazienza⌉`: chi trova più di K auto già in cerca rinuncia (conta come "non trovato"). Stabile per ogni carico, continua attraverso ρ = 1, coincide con la formula M/M/c quando K → ∞ e ρ < 1 (testato). Ne derivano posti occupati attesi `E[min(n, c)]`, liberi `c − occupati`, `P(posto entro 5 minuti)`.
- Incertezza: 40 estrazioni Monte Carlo (seme 49) dei parametri, triangolari su [minimo, massimo] con moda = valore centrale; intervallo 5°–95° percentile. I totali di città sommano per estrazione, poi i percentili.

**Parametri principali** (tutti in `city.yaml`, valore centrale [min–max]):

| Parametro | Valore | Dato / ipotesi | Fonte |
|---|---|---|---|
| Residenti per NIL | 1.399.079 (2025) | dato | ds27, ds964 |
| Auto dei residenti | 684.613 (2022) | dato | ds1094 (2023 escluso: salto a 1,85 milioni), coincide con ds721 |
| Ingressi auto in Area C, profilo | per giorno e fascia | dato | ds1072 (2023-24), ds818 (2016), varchi ds82 |
| Unità locali per NIL | 182.833 (2010) | dato vecchio | ds201 |
| Festivi | nazionali + 7 dicembre | dato | calendario |
| Lunghezza stallo | 5,0 m [4,8–5,5] | ipotesi | — |
| Lati con sosta | 1,5 [1,0–1,9] | ipotesi | nessuna larghezza delle strade |
| Quota sostabile | 0,6 [0,45–0,75] | ipotesi | — |
| Arretramento dagli incroci | 5 m | ipotesi (regola CdS non verificata alla fonte) | — |
| Sovrapposizione aree mappate | 0,3 [0–0,6] | ipotesi | — |
| Quota moto del marciapiede | 0,03 [0,01–0,05] | ipotesi | — |
| Auto dei residenti in strada | 0,45 [0,3–0,6] | ipotesi | — |
| Quota fuori casa al picco | feriale 0,4, sabato 0,3, festivo 0,2 | ipotesi | — |
| Durata fuori casa | 7 h [4–9] | ipotesi | — |
| Ingressi in cordone che sostano in strada | 0,3 [0,15–0,45] | ipotesi | — |
| Moltiplicatore fuori cordone | 2 [1–4] | ipotesi | — |
| Soste di lavoro / durate | 0,3; 8 h; breve 75 min | ipotesi | — |
| Pazienza di ricerca | 10 min [5–20] | ipotesi | — |

**Primo risultato (Milano, feriale, stima non verificata):** capacità 386.000 posti auto [290.000–448.000], 46.000 stalli moto [24.000–69.000]; occupati alle 10 circa 241.000 [199.000–273.000]. Controlli di plausibilità superati di poco: capacità/auto dei residenti 0,56; occupazione alle 3 di notte 0,62 (soglia 0,6); visitatori/auto fuori casa alle 10: 0,53.

**Calibrazione con le segnalazioni:** per ogni zona un fattore di scala `s` della domanda (moltiplica carico e arrivi). Prior `log s ~ N(0; 0,5)`; verosimiglianza Bernoulli degli esiti "trovato entro 5 minuti" con `P(s)` del modello; posteriore su griglia (`calibrate_demand_scale`). Su esiti sintetici con s = 1,5 noto il codice lo recupera: verifica del codice, **non** dell'accuratezza. Su esiti reali il fattore si stima con dati tenuti da parte (§6) e la calibrazione si misura come in §6.

**Limiti dichiarati:** auto per residente uniforme in città (il centro ne ha meno); flotte aziendali forse incluse nel parco; unità locali del 2010 su confini NIL di oggi; profilo di Area C applicato a tutta la città; partenze dei residenti modellate con lo stesso profilo degli ingressi (anche serali); pendolari da fuori città rappresentati solo dal moltiplicatore; regole di sosta, tariffe, strisce gialle e lavaggio strade assenti (T-041); un giorno tipo ripetuto (nessun effetto venerdì → sabato); `μ = λ/a` è esatto solo a regime; la coda FIFO approssima una ricerca che in strada è disordinata.

**Cosa non sappiamo ancora:** la quota di auto dei residenti che dorme in strada (pesa più di tutto); la larghezza delle strade e quindi i lati con sosta; quanti visitatori arrivano fuori dal cordone; se l'occupazione notturna del 62% è troppo bassa (l'esperienza nei quartieri semicentrali suggerisce di sì). Servono esiti reali per cella e fascia, e conteggi a campione di auto in sosta su alcuni tratti (bozza di protocollo da preparare con `qa-tester`).
