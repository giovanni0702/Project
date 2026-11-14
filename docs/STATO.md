# STATO

Aggiornato: 2026-11-14 · Iterazione **1 (in corso)** · Cicli autonomi: martedì e venerdì alle 03:41 in una sessione dedicata (D-032), procedura in `17-autonomia.md`.

## Ultimi fatti
1. **SostaMi versione web** (D-035, D-036): mappa vera di Milano dai dati del Comune, ricerca vie, veicolo, sosta salvata, segnalazioni sul dispositivo, "Dove sono". Privata: https://claude.ai/artifact/RCK6XaPgv7oTuTKun7Wk87. Sito pronto in `site/`, da pubblicare da un repository separato (D-038).
2. **Modello di occupazione** (D-037, `09-modello.md` §11): posti totali, occupati, liberi e probabilità per zona e fascia, con intervalli; collegato alla mappa. **Non verificato e troppo ottimista in centro** (T-050).
3. **Dati:** 30.727 tratti di strada, 3.090 aree di sosta, 74 parcheggi in struttura, edifici, verde, acqua (Database Topografico del Comune, CC BY). Capacità stimata: circa 386.000 posti auto (290.000–448.000).
4. **Backend** in `backend/` (locale). **Privacy:** 5 falle chiuse (T-040), verifica indipendente da fare (T-047); 75+ test verdi.
5. Nome SostaMi e logo (D-033, marchio da verificare T-048); grafica in `16-grafica.md`; marketing in `11-marketing.md`.
6. Beta su tutto il Comune (D-029): stima a livelli da costruire (T-045).

## Cosa sappiamo
- Nessuna fonte pubblica in tempo reale sulla sosta su strada; i dati di Google non si possono usare (D-004, D-037).
- OpenStreetMap non raggiungibile dalla sessione; Milano usa i dati del Comune.
- Mancano fonti per tariffe, orari, lavaggio strade, stalli moto reali.

## Proposte per il fondatore
1. Conteggi a campione delle auto in sosta su 20 strade (un'ora di lavoro di una persona): è il modo più rapido per verificare il modello.
2. Collegare la versione web al servizio appena firmata la DPIA: le prime segnalazioni calibrano il modello.
3. Mostrare l'intervallo di incertezza anche sulla mappa (colore più tenue dove il modello è incerto).

## Prossimi passi
1. Azioni del fondatore per pubblicare il sito (D-038); poi copia di `site/` e verifica.
2. T-050 (modello credibile), T-047 (red team), T-045 (stima a livelli), T-044 (web collegata al servizio).
3. T-041 (sosta lungo il marciapiede, moto, tariffe), T-048 (marchio), T-030 (servizio online gratuito).

## Blocchi
- Pubblicazione del sito: 4 azioni del fondatore. T-042: testi di legge non raggiungibili.
