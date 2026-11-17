# T-050 — Diagnosi del modello di occupazione e protocollo dei conteggi a campione

> **Stime del modello, NON verificate.** Nessun numero qui è una misura. Fonte esterna di confronto: nessuna disponibile (vedi §3). Riferimento: `docs/09-modello.md` §11.

Data: 2026-11-17 · Riproduzione: `scripts/build_occupancy.py milano` (seme 49, 40 estrazioni); parametri in `cities/milano/city.yaml`.

## 1. Diagnosi: perché il centro risultava facile

Feriale, valori centrali per quartiere (NIL), media pesata sulla capacità. "Occ." = auto in sosta / posti; "P" = probabilità di posto entro 5 minuti.

| Quartiere | Classe | Posti prima → dopo | Occ. 03:00 prima → dopo | Occ. 11:00 prima → dopo | P 11:00 prima → dopo | P 03:00 prima → dopo |
|---|---|---|---|---|---|---|
| Duomo | centro | 6.511 → 4.590 | 0,65 → 0,96 | 0,74 → 0,99 | 100% → 49% | 100% → 82% |
| Brera | centro | 4.671 → 3.491 | 0,78 → 0,95 | 0,82 → 0,97 | 100% → 45% | 100% → 64% |
| Buenos Aires - P.ta Venezia | semicentro denso | 9.994 → 9.993 | 0,99 → 1,00 | 0,99 → 1,00 | 27% → 16% | 54% → 37% |
| Sarpi | semicentro denso | 4.707 → 4.598 | 0,97 → 0,99 | 0,98 → 0,99 | 44% → 26% | 63% → 42% |
| Loreto - Casoretto - NoLo | semicentro denso | 4.048 → 4.047 | 1,00 → 1,00 | 1,00 → 1,00 | 14% → 10% | 28% → 20% |
| De Angeli - Monte Rosa | semicentro | 5.130 → 5.129 | 0,85 → 0,92 | 0,86 → 0,92 | 84% → 65% | 91% → 75% |
| Quarto Oggiaro | periferia | 7.661 → 7.662 | 0,74 → 0,81 | 0,71 → 0,79 | 97% → 84% | 95% → 82% |
| Gratosoglio | periferia | 6.417 → 6.414 | 0,52 → 0,61 | 0,49 → 0,58 | 100% → 99% | 99% → 98% |
| **Città** | — | 386.084 → 380.332 | 0,62 → 0,69 | 0,62 → 0,67 | 87% → 78% | 91% → 82% |

Cause trovate (in ordine di peso):
1. **Pochi residenti per posto in centro.** Duomo e Brera hanno 500–670 residenti per km di cordolo utile contro 1.100–1.700 del semicentro denso: con la stessa quota di auto in strada (0,45) il centro di notte restava al 65–78%. In centro la sosta è riempita anche da auto non intestate ai residenti (leasing, aziendali) e da veicoli commerciali, assenti nel modello.
2. **Capacità sovrastimata in centro.** Stessa geometria del resto della città (1,5 lati, quota sostabile 0,6), ma nel cordone pesano binari del tram, vie pedonali e ZTL, carico e scarico, taxi, car sharing, stalli disabili.
3. **Coda molto "netta" con molti posti per cella.** Con centinaia di posti per cella H3, P resta vicino al 100% finché l'occupazione media non supera circa 0,95: sotto quella soglia un posto libero si trova sempre. Il problema era quindi l'occupazione troppo bassa, non la formula.
4. **Visitatori del centro.** Stimati dagli ingressi in Area C (0,26–0,33 dei posti alle 11). Non sono cambiati: nessuna fonte per correggerli.
5. **Stalli riservati ai residenti (strisce gialle).** Non modellati: per un visitatore la capacità utile è minore. Struttura rinviata (servono le quote per ambito; `sosta_ambiti.geojson` ha solo i perimetri, campi posti vuoti).

## 2. Correzioni (tutte ipotesi dichiarate in `city.yaml`, con intervallo)

| Parametro | Valore [min–max] | Effetto |
|---|---|---|
| `core_capacity_factor` | 0,7 [0,55–0,85] | quota del cordolo che resta sostabile nel cordone (Area C) |
| `unregistered_car_factor` | 1,1 [1,0–1,3] | auto tenute in città ma intestate altrove; la rottura di serie 2023 di ds1094 (1,85 milioni) indica flotte grandi, non quantificate |
| `goods_on_street_share` | 0,5 [0,3–0,7] | quota in strada di notte dei 64.214 autocarri (ds721, 2022, **dato**) |

Codice: `resident_vehicles`, `zone_table`, `plausibility_checks` in `scripts/build_occupancy.py`; test in `tests/test_occupancy_checks.py` (sintetici: verificano il codice, non l'accuratezza).

**Controlli automatici** (soglie = attese dichiarate, non misure; in `occupancy_checks` di `city.yaml`): occupazione notturna di città ≥ 0,6 (0,69); notte nei quartieri residenziali densi ≥ 0,85 (1,00); P alle 11 in centro ≤ 0,6 (0,47); P in centro almeno 20 punti sotto la periferia (−0,44). Tutti superati: significa solo che l'output non è più palesemente implausibile.

**Restano dubbi:** il semicentro denso di giorno risulta più difficile che di notte (visitatori stimati ≈ 0,35 dei posti, moltiplicatore fuori cordone 2): da verificare con i conteggi. In Brera 2 celle su 18 restano al 100% (celle di bordo con pochi residenti).

## 3. Fonte esterna

Nessuna utilizzabile tra quelle già citate in `docs/fonti.md`: "La sosta a Milano" (circa 39.000 stalli pubblici) è secondaria e non dice che cosa conta; dati AMAT non raggiungibili. **Criterio aperto.**

## 4. Protocollo dei conteggi a campione (bozza, da concordare con `qa-tester`)

**Scopo:** confrontare l'occupazione osservata con quella del modello nella cella, in centro, semicentro e periferia.
**Strade (20 tratti di 100–200 m, nomi presenti nel grafo stradale; verificare sulla mappa prima di uscire):**
- Centro (6): Via Solferino, Via San Marco, Via Pontaccio, Via Borgonuovo, Via Santa Marta, Via Lanzone.
- Semicentro denso (7): Via Lecco, Via Melzo, Via Lazzaretto, Via Bramante, Via Luigi Canonica, Via Luigi Varanini, Via Arqua.
- Semicentro (2): Via Giorgio Washington, Via Mose Bianchi.
- Periferia (5): Via Cesare Pascarella, Via Val Di Bondo, Via Michele Lessona, Via Michele Saponaro, Via Dei Missaglia.

**Come (circa 3 minuti per tratto, a piedi):** per ogni tratto e lato: auto in sosta regolare; auto in sosta irregolare (doppia fila, strisce, passi carrai); spazi liberi regolari di almeno 5 m; tipo di strisce (blu, gialle, bianche). Annotare via, da–a, lato, data, ora di inizio.
**Quando:** feriale 10:30–12:00 e feriale 22:30–24:00 (proxy della notte). Un'ora di conteggio copre un gruppo di 5–7 tratti vicini; i 20 tratti richiedono 4 uscite brevi o un'ora di conteggio più gli spostamenti.
**Privacy:** nessuna targa, nessuna foto di persone o targhe, solo conteggi aggregati per tratto.
**Confronto:** occupazione osservata = (regolari + irregolari) / (regolari + liberi); si confronta con l'intervallo del modello per la cella e la fascia. Si riportano: quota di tratti dentro l'intervallo, segno della differenza centro–periferia, errore medio per classe. Criterio di successo da fissare con `product-manager` **prima** dei conteggi. Pochi tratti non calibrano il modello: servono a scoprire errori grossi.

## Cosa non sappiamo ancora
Quota reale di auto dei residenti in strada; quante auto non intestate ai residenti dormono in città; capacità vera del centro (stalli, ZTL, binari); quota di stalli gialli per ambito; visitatori fuori dal cordone. Nessuna di queste ipotesi è verificata.
