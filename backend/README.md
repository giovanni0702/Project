# Backend beta (locale, costo zero, D-014)

FastAPI + SQLite (libreria standard). Una istanza serve una città (`PARKING_CITY`, da `cities/<id>/city.yaml`).

## Avvio
```
PARKING_CITY=<id> .venv/bin/python -m backend        # 127.0.0.1:8000, access log spento (C7)
PARKING_CITY=<id> .venv/bin/python -m backend.publish_job <id> --retention
```
Variabili: `PARKING_DB` (default `data/backend/events.sqlite3`), `PARKING_OUT` (default `build/grid`).

## Endpoint
- `POST /v1/events` → 202. Campi ammessi: `type` (solo `parked`: le ripartenze non si raccolgono), `cell` (H3 della città), `slot_day_type`, `slot_index`, `search_bucket` (0-3, solo parked), `vehicle_class` (opzionale, solo contatori aggregati, mai salvata con l'evento), `pid` (20 hex), `app_version`. Campi extra → 422; duplicato (pid, tipo, cella, giorno) → 429 (C9).
- `GET /v1/grid/{city}` e `/v1/forecast/{city}`: file statici del job di pubblicazione.

## Cosa si salva
Storico: cella, fascia, scaglione, pid e **settimana** (lunedì); `app_version` e taglia non si salvano. Tabelle a breve vita: `live` (passo di 5 min, fino a `live_window_minutes`), `daily_seen` (1 giorno). Contatori `vehicle_outcomes` (settimana, taglia, scaglione). Niente ora di arrivo, IP o user-agent (C5, C7). Tabella `admitted`: stato di ammissione a blocchi (C6), mai pubblicato.

## Pubblicazione
Il job legge gli eventi, li converte in esiti (successo = scaglione 0 o 1), applica ammissione e soglia k, scrive `grid.json` (adesso) e `forecast.json` (stime per fascia e tipo di giorno, senza "adesso"; elenca solo le celle diverse dal valore `default`). Nessun pid né conteggio nei file. Da eseguire ogni `publish.interval_minutes` (cron).

## Retention
`--retention` cancella eventi e ammissioni oltre `privacy.raw_retention_days`.

## Limiti noti
Nessuna autenticazione né TLS (solo locale). Il ritardo casuale (C7) è sul telefono. Per PostgreSQL: implementare `EventStore` in `backend/store.py`.
