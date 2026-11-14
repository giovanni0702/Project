# Fonti — cache delle ricerche web

Se WebFetch non raggiunge un sito consentito: `scripts/fetch_text.py <url>`, poi Grep sul file salvato. Prima di una ricerca: Grep qui. Dopo: una riga per fonte. Scadenza: 90 giorni per policy, prezzi e concorrenti; 180 per dati e norme. Una fonte scaduta va riletta.
Stato: **letta** (pagina ufficiale aperta) · **parziale** (troncata o solo titolo) · **secondaria** (snippet o terzi) · **bloccata** (host non raggiungibile).

| Tema | URL | Data | Stato | Risultato |
|---|---|---|---|---|
| Dati | dati.comune.milano.it (catalogo) | 2026-11-14 | bloccata | Nessun dataset di stalli o sensori nei risultati di ricerca; tariffe per ambito CC BY 4.0 (agg. 2025-04-03) |
| Dati | mobilitydatabase.org/feeds/gtfs/mdb-2666 | 2026-11-14 | secondaria | GTFS ATM (ds929), validità osservata fino al 2026-06-12 |
| Dati | istat.it/it/archivio/104317 | 2026-11-14 | secondaria | Basi territoriali 2021, CC BY 4.0 |
| Dati | open-meteo.com/en/terms | 2026-11-14 | secondaria | Dati CC BY 4.0; API gratuita solo per uso non commerciale |
| Dati | partecipazione.comune.milano.it (PDF "La sosta a Milano") | 2026-11-14 | secondaria | Circa 39.000 stalli pubblici: stima, non usare come input |
| Google | cloud.google.com/maps-platform/terms | 2026-11-14 | parziale | Testo corrente non letto (sez. 3.2.3 da leggere) |
| Google | cloud.google.com/maps-platform/terms/maps-service-terms/index-20240522 | 2026-11-14 | letta (archiviata) | Cache di lat/lng 30 giorni; divieto d'uso di alcuni contenuti con mappe non Google |
| Google | developers.google.com/maps/documentation/urls/get-started | 2026-11-14 | bloccata | Deep link non verificati |
| Google | developers.google.com/maps/billing-and-pricing/pricing | 2026-11-14 | secondaria | Soglie gratuite per servizio; nessun tetto di spesa automatico |
| Norme | developer.apple.com (DSA compliance, App Store Connect) | 2026-11-14 | secondaria | Apple verifica e mostra i contatti dei venditori UE |
| Norme | Direttiva (UE) 2019/882 (EAA) | 2026-11-14 | secondaria | Esenzione microimprese per i servizi: probabile, testo non letto |
| Norme | garanteprivacy.it | 2026-11-14 | secondaria | Nessuna linea guida recente specifica sulla localizzazione nelle app; EDPB 1/2022 non lette |
| Store | developer.apple.com/app-store/review/guidelines/ | 2026-11-14 | parziale | 5.1.1, 5.1.2, 5.1.5 letti; consenso anche per dati anonimi |
| Store | developer.apple.com/app-store/app-privacy-details/ | 2026-11-14 | letta | Posizione "approssimativa" se arrotondata prima del salvataggio |
| Store | developer.apple.com/programs/enroll/ | 2026-11-14 | letta | 99 USD l'anno |
| Store | developer.android.com/google/play/requirements/target-sdk | 2026-11-14 | letta | Target API 36 dal 2026-08-31 |
| Store | support.google.com/googleplay/android-developer (9799150, 10787469, 14151465, 6112435) | 2026-11-14 | bloccata | Posizione in background, Data safety, tester chiusi, costo: non verificati |
| Concorrenti | sicurauto.it (FindPark a Milano) | 2026-11-14 | secondaria | FindPark sembra essere Find & Park di EasyPark |
| Concorrenti | business.parkopedia.com/blog (predictions) | 2026-11-14 | secondaria | Previsioni su strada solo B2B |
| Concorrenti | apps.apple.com/us/app/id897809583 | 2026-11-14 | secondaria | SpotAngels attiva in città USA: avvisi pulizia strade, posizione dell'auto |
| Concorrenti | trustpilot.com (EasyPark Italia) | 2026-11-14 | secondaria | Tema ricorrente: multe nonostante la sosta pagata |
| Concorrenti | parkingmycar.it/blog/pulizia-strade-milano | 2026-11-14 | secondaria | Calendario pulizia strade su blog; app PuliAMO non confermata |
| Costi | docs.hetzner.com (price adjustment) | 2026-11-14 | secondaria | Rincaro dal 15 giugno 2026; server piccoli circa 4,5–6,5 €/mese |
| Costi | developers.cloudflare.com/r2/pricing | 2026-11-14 | secondaria | Gratis 10 GB, uscita dati gratuita; residenza UE non verificata |
| Costi | neon (blog di terzi) | 2026-11-14 | secondaria | Piano gratuito limitato; PostGIS e regione UE non verificati |
| Costi | maptiler.com/cloud/pricing | 2026-11-14 | secondaria | Piano gratuito solo non commerciale; a pagamento da circa 25 $/mese |
| Google | cloud.google.com/maps-platform/terms | 2026-11-14 | letta | Sez. 3.2.3: vietati estrazione, cache, contenuti derivati, uso dei servizi con mappe non Google |
| Google | developers.google.com/maps/documentation/urls/get-started | 2026-11-14 | letta | I link a Google Maps non richiedono chiave API |
| Licenze | opendatacommons.org/licenses/odbl/1-0/ | 2026-11-14 | letta | Definizioni di database derivato e di opera prodotta; l'opera prodotta richiede solo l'avviso. Interpretazione sul nostro caso: parere legale |
| Store | support.google.com/googleplay/android-developer/answer/14151465 | 2026-11-14 | letta | Account personali: test chiuso con almeno 12 tester per 14 giorni prima della produzione |
| Store | support.google.com/googleplay/android-developer/answer/6112435 | 2026-11-14 | letta | Registrazione Google Play: 25 USD una tantum |
| Store | support.google.com/googleplay/android-developer/answer/9799150 | 2026-11-14 | letta | Posizione in background solo se essenziale alla funzione principale, con dichiarazione e approvazione |
| Store | developer.android.com/developer-verification/guides/faq | 2026-11-14 | letta | Verifica sviluppatore: dal 2026-09-30 in 4 paesi, globale nel 2027; account limitato gratuito fino a 20 dispositivi |
| Store | developer.android.com/training/location/permissions | 2026-11-14 | letta | Permessi di posizione; background dalle impostazioni su Android 11+ |
| Dati | dati.comune.milano.it/api/3 (ricerche: sosta, parcheggi, area c, mercati) | 2026-11-14 | letta | 2617 dataset; nessuno su stalli, sensori, tariffe, lavaggio strade; presenti ds83, ds342, ds45, ds82, ds574, mercati |
| Dati | dati.comune.milano.it/gtfs.zip | 2026-11-14 | letta | GTFS valido 2026-10-26 / 2026-11-30 |
| Dati | bikemi.com/en/open-data/realtime | 2026-11-14 | secondaria | GBFS ogni 10 secondi |
| Dati | developer.tomtom.com/pricing | 2026-11-14 | secondaria | 2.500 richieste al giorno gratis; termini su conservazione e modelli da leggere |
| Dati | open-meteo.com/en/pricing | 2026-11-14 | secondaria | Gratis solo non commerciale; commerciale circa 29 USD/mese |
| Dati | ATM, posti liberi dei parcheggi di interscambio | 2026-11-14 | secondaria | Nessun feed pubblico in tempo reale |
| Costi | pub.dev/packages/maplibre (e changelog) | 2026-11-14 | letta | Versione 0.3.7+1; PMTiles su Android dalla 0.2.1 |
| Costi | Neon, Supabase, Cloudflare R2/Pages (pagine ufficiali non raggiungibili) | 2026-11-14 | secondaria | Piani gratuiti esistono; regione UE, PostGIS, carta richiesta: non verificati. Pages: 25 MiB per file |
