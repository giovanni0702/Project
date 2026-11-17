# 14 — Valutazione degli agenti

Si aggiorna a ogni chiusura di iterazione (`ceo-orchestrator`). Voto da 1 a 5 su: utilità del risultato, onestà su ciò che non è verificato, rispetto del perimetro, costo.

## Ciclo 1 — 2026-11-14 (10 incarichi, circa 455.000 token dei sub-agenti, più l'incarico privacy in corso)

| Agente | Incarichi | Voto | Cosa ha funzionato | Cosa migliorare |
|---|---|---|---|---|
| data-engineer | 2 | 4 | Ha trovato l'accesso al catalogo del Comune e ha corretto un proprio errore del primo giro | Nel primo giro ha riportato come fatto un dato visto solo in un'anteprima (dataset tariffe): mai senza marcarlo |
| release-manager | 2 | 4 | Scoperta utile e verificata: beta Android gratuita e regole 2026–2027 | Costoso (70.000 token); parte dei requisiti scritti a memoria |
| competitor-analyst | 1 | 3 | Ha capito che FindPark è Find & Park di EasyPark | Non ha letto gli store (rete); recensioni da fonti indirette |
| privacy-compliance | 2 | 3 | Sempre chiaro su cosa non era verificato; pareri prudenti | Secondo giro: pareri solo a memoria, si è fermato al primo sito irraggiungibile senza poter usare altre vie |
| privacy-compliance (DPIA) | 1 | 5 | Ha usato il veto con motivazioni concrete e ha proposto 12 correzioni attuabili; ha trovato due falle reali (differenza tra griglie consecutive; identificatore a 24 ore che lascia contare una persona più volte) | Norme non lette alla fonte (domini non abilitati); non ha potuto eseguire `make check` |
| generico (costi) | 2 | 2 | Tabella leggibile, raccomandazione chiara | 157.000 token per dati quasi tutti di seconda mano: il peggior rapporto costo/valore |
| Tutti gli altri ruoli | 0 | — | Non usati: il lavoro è stato fatto direttamente, perché costava meno | Da valutare al primo incarico |

## Ciclo 2 — 2026-11-14 (5 incarichi, circa 190.000 token più T-040 in corso)

| Agente | Voto | Motivo |
|---|---|---|
| privacy-redteam | 5 | 5 falle reali dimostrate con test riproducibili, più una non richiesta; perimetro rispettato |
| data-scientist | 5 | Ha detto chiaramente, con numeri, che la configurazione attuale non mostra mai dati reali; proposta concreta |
| backend-engineer | 4 | Backend completo e provato in un solo giro a basso costo; ha però salvato giorno e taglia, da cui due delle falle |
| legal-analyst | 3 | Onesto su ciò che non ha letto (9 su 13); bloccato da siti che restituiscono pagine vuote, tetto di chiamate rispettato |
| privacy-engineer | 4 | 5 falle chiuse con costo dichiarato per la stima; ha però adattato lui i test del red team: serve verifica indipendente (T-047). Costoso (103.000 token) |
| marketing-sales | 4 | Piano concreto a costo zero, vincoli privacy rispettati, nessuna ricerca inutile; nomi e obiettivi non verificati |

Lezione del ciclo: il red team va lanciato **dopo** ogni nuovo flusso di dati, non in parallelo, così attacca anche il codice appena scritto.

## Ciclo 3 — 2026-11-14

| Agente | Voto | Motivo |
|---|---|---|
| data-scientist (occupazione) | 4 | Modello completo, formule corrette e testate, incertezza dichiarata, ipotesi elencate; risultato però poco plausibile in centro e costo alto (124.000 token) |

## Ciclo 4 — 2026-11-17

| Agente | Voto | Motivo |
|---|---|---|
| privacy-redteam (T-047) | 5 | Tre attacchi riusciti trovati e fissati come test, nessun codice di produzione toccato, 12 chiamate e 48.000 token; campione D/E piccolo, dichiarato |
| data-scientist (T-050) | 4 | Diagnosi con cause e numeri prima/dopo, parametri in configurazione, limiti dichiarati (0 fonti); restano incoerenze nel semicentro, 80.000 token |

## Problemi di sistema (e correzioni applicate)
1. **Ricerche lanciate prima di controllare la rete.** Il primo giro (5 incarichi, circa 213.000 token) ha prodotto risultati parziali perché i siti ufficiali erano bloccati. *Errore di chi ha delegato, non degli agenti.* Correzione: prima di ogni ricerca si prova un sito con `scripts/fetch_text.py`.
2. **Lo strumento di lettura web degli agenti non raggiunge siti che lo script raggiunge.** Correzione: `privacy-compliance` e `competitor-analyst` ora possono usare Bash, solo per `scripts/fetch_text.py` e `make check`.
3. **Fatti presi da anteprime di ricerca.** Correzione: regola in ogni agente di ricerca, "un'anteprima non è una fonte letta".
4. **Scrittura a memoria su norme e policy.** Correzione: ogni affermazione normativa non letta alla fonte porta **[verificare]**; i pareri a memoria si dichiarano tali nella prima riga.
5. **Incarichi di ricerca generici costosi.** Correzione: ricerche su prezzi e fornitori solo con elenco chiuso di pagine da leggere e tetto di 8 chiamate.

## Rinforzi decisi dal fondatore
- Team privacy (D-025): tre specialisti sotto `privacy-compliance`, per coprire i due limiti emersi (fonti non lette, nessun attacco reale alle protezioni).
- `visual-designer` (D-020).

## Come si valuta dal prossimo ciclo
- Ogni report di agente chiude con una riga: `Verificato alla fonte: N · Non verificato: M · Chiamate: K`.
- Chi delega annota qui, in una riga, voto e motivo.
- Due voti ≤ 2 consecutivi: si riscrive la definizione dell'agente o si cambia modello (D-008).
