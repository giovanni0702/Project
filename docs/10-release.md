# 10 - Release e requisiti degli store

Ultima verifica: 2026-11-14 (release-manager, T-003, ripresa). Le voci **[verificare]** non sono confermate su pagina ufficiale.
Nota: `support.google.com`, `play.google.com` e `firebase.google.com` non risolvono il DNS dalla sessione (fuori dai domini consentiti). Letti solo developer.android.com e developer.apple.com.

## 1. Profilo dell'app (base per i requisiti)
- Flutter, iOS + Android. Localizzazione **solo in uso** (foreground); background solo opzionale, off di default.
- Raccoglie eventi anonimi di parcheggio (posizione approssimata/arrotondata, orario, nessun ID utente stabile).
- Nessun tracking, nessuna pubblicità, nessun account (da confermare con `privacy-compliance`).

## 2. Apple App Store
| Tema | Requisito | Fonte | Verifica |
|---|---|---|---|
| 5.1.1(i) | Link alla privacy policy in App Store Connect e dentro l'app. La policy deve dire cosa si raccoglie, come, per cosa, ritenzione/cancellazione e come revocare il consenso | https://developer.apple.com/app-store/review/guidelines/ | 2026-11-14 |
| 5.1.1(ii) | Consenso richiesto anche per dati "anonimi"; modo semplice per revocarlo; purpose string chiare e complete. Il trattamento per legittimo interesse GDPR deve rispettare la legge | idem | 2026-11-14 |
| 5.1.1(iii)-(iv) | Minimizzazione; alternativa se l'utente nega la posizione (es. inserire un indirizzo a mano) | idem | 2026-11-14 |
| 5.1.2(i)-(ii) | Nessun uso/condivisione di dati personali senza permesso; no riuso per scopi diversi senza nuovo consenso; non si può obbligare ad attivare la posizione per usare l'app | idem | 2026-11-14 |
| 5.1.5 | Posizione solo se direttamente rilevante; avviso e consenso prima di raccogliere/trasmettere | idem | 2026-11-14 |
| 2.5.4 | Servizi in background solo per lo scopo previsto (incluso "location") | idem | 2026-11-14 |
| Data di ultimo aggiornamento delle Guidelines | Non letta (pagina troncata, ultimi ~14k caratteri non letti) | idem | **[verificare]** |
| Background location | Le Guidelines lette non hanno una regola dedicata; la giustificazione si dà nel testo della purpose string e nelle note di review | idem | **[verificare]** nelle note per il revisore |

### Purpose strings (Info.plist)
- Chiavi: `NSLocationWhenInUseUsageDescription` (obbligatoria); `NSLocationAlwaysAndWhenInUseUsageDescription` solo se si chiede "Always". Senza la chiave l'app termina alla richiesta.
- Regole (da documentazione): spiegare il beneficio per l'utente, essere specifici, coerenti col comportamento reale, brevi, localizzate IT/EN in `InfoPlist.strings`.
- Pagina: https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationwheninuseusagedescription | 2026-11-14 | la pagina e' stata letta solo come titolo; contenuto da conoscenza generale: **[verificare]**.

### App Privacy (nutrition labels)
Fonte: https://developer.apple.com/app-store/app-privacy-details/ (2026-11-14, letta).
- Precise Location = 3 o piu' decimali; Coarse = risoluzione inferiore. Se si raccoglie preciso ma si arrotonda subito prima di salvare, si dichiara **Coarse Location**.
- "Linked to you" salvo dati de-identificati prima della raccolta; vietato ri-collegarli dopo.
- Dati raccolti con continuita' dopo il permesso vanno dichiarati (la deroga "opzionale" non si applica).
- Vanno inclusi i dati raccolti dagli SDK di terze parti. Risposte modificabili senza nuova build. Obbligatorie per nuove app e aggiornamenti.
- Bozza: Location > Coarse Location, scopo App Functionality (+ Analytics solo se vero), non linked, non tracking. Da validare con `privacy-compliance`.

### Privacy manifest (`PrivacyInfo.xcprivacy`)
- Fonte: https://developer.apple.com/documentation/bundleresources/privacy-manifest-files | 2026-11-14 | pagina letta solo come titolo; dettagli da conoscenza generale: **[verificare]**.
- Da conoscenza generale: obbligatorio dal 2024-05-01 per nuove app e aggiornamenti; dichiara tracking, domini, tipi di dati raccolti e required-reason APIs (es. UserDefaults, file timestamp). Ogni SDK/plugin Flutter deve avere il proprio manifest.

### Costo account
- Apple Developer Program: 99 USD/anno (individuale: serve Apple Account con 2FA, nome legale, maggiore eta'). Fonte: https://developer.apple.com/programs/enroll/ | 2026-11-14. Account da creare dal fondatore.

## 3. Google Play
| Tema | Requisito | Fonte | Verifica |
|---|---|---|---|
| Target API | Dal 2026-08-31 nuove app e aggiornamenti devono targetare API 36 (Android 16). La proroga al 2026-11-01 e' scaduta: oggi serve API 36 | https://developer.android.com/google/play/requirements/target-sdk | letta 2026-11-14 |
| Permessi posizione (policy) | Dichiarazione permessi, prominent disclosure in-app prima del prompt, video per background location | https://support.google.com/googleplay/android-developer/answer/9799150 | **[verificare]** bloccata |
| Background location | `ACCESS_BACKGROUND_LOCATION` solo se la funzione core lo richiede; form e revisione dedicata. Da evitare in beta e v1 | stessa pagina; developer.android.com/training/location/permissions (letta) | policy **[verificare]**; tecnica letta 2026-11-14 |
| Android 11+ | Foreground e background chiesti separatamente; il background si concede dalle impostazioni, non dal dialog | developer.android.com/training/location/permissions (letta) | 2026-11-14 |
| Android 12+ | `ACCESS_COARSE_LOCATION` sempre insieme a `FINE`; l'utente puo' concedere solo l'approssimata: l'app deve funzionare anche cosi' | idem | 2026-11-14 |
| Data safety | Obbligatoria per tutte le app, coerente con il comportamento reale e con la privacy policy | https://support.google.com/googleplay/android-developer/answer/10787469 | **[verificare]** bloccata |
| Test chiusi per account personali nuovi | Memoria: 12 tester per 14 giorni prima di chiedere la produzione | https://support.google.com/googleplay/android-developer/answer/14151465 | **[verificare]** bloccata |
| Costo account | Memoria: 25 USD una tantum. La FAQ di verifica sviluppatore Android (letta 2026-11-14) cita "Play's $25 registration fee" come riferimento | https://support.google.com/googleplay/android-developer/answer/6112435 | importo **parziale**; pagina ufficiale **[verificare]** |

Scelta consigliata: nella v1 NON dichiarare background location (meno revisione, meno rischio). Se mai servira', aprire un task dedicato prima.

## 3bis. Beta Android a costo zero (decisione fondatore: solo Android, nessuna spesa, APK diretto)

**Esito: fattibile, sì.** Oggi un APK firmato e non registrato si installa in Italia. La verifica sviluppatore Android parte il 2026-09-30 solo in Brasile, Indonesia, Singapore e Thailandia, ed e' annunciata a livello globale per il 2027 (FAQ letta). Il 2027 e' il rischio principale.

### Verifica sviluppatore Android (developer.android.com, letta 2026-11-14)
- **Obbligatorieta':** dal 2026-09-30 solo negli store partecipanti di quattro paesi. Gli APK distribuiti direttamente non sono coperti da quella scadenza. L'Italia non e' citata. Estensione globale nel 2027, mese non indicato: **[verificare]**.
- **Costo:** account completo 25 USD (Android Developer Console, "similar to Play's $25 registration fee"), con documento d'identita' governativo. Esonerato per l'account limitato.
- **Account a distribuzione limitata:** gratuito, senza documento, fino a 20 dispositivi, per studenti e hobbisti, lancio agosto 2026. Conversione solo verso l'account completo. Procedura di creazione e necessita' di un account Play Console **[verificare]**.
- **Dal 2027 (da confermare):** app non registrate installabili solo con "advanced flow" (modalita' sviluppatore, attesa di 24 h, riavvio, conferma biometrica, poi avviso "Installa comunque") o via ADB. Con advanced flow disattivato, gli aggiornamenti delle app non registrate falliscono.
- **Firma:** chiave persa = pacchetto non registrabile. Keystore del fondatore fuori dal repo, con backup offline.

### Passi
1. Fondatore: decide se aprire l'account limitato ora (gratuito, consigliato) o piu' avanti. L'agente non crea account.
2. Fissare `applicationId` definitivo (cambiarlo perde gli aggiornamenti) e `versionCode` crescente.
3. Build APK release con target API 36 e firma v2 (obbligatoria da Android 11, letta) con il keystore del fondatore. Nessuna chiave nel bundle.
4. `qa-tester`: test su un dispositivo Android reale e un emulatore API 36 (installazione, permessi, rifiuto posizione).
5. Il fondatore invia l'APK e il SHA-256 ai tester con un canale privato a sua scelta. Invio = decisione riservata (CLAUDE §7).
6. Istruzioni IT/EN per i tester: attivare "Installa app sconosciute" per il gestore file o il browser; se compare l'avviso Play Protect, scegliere "Installa comunque". Testo esatto dell'avviso **[verificare]** su device.
7. Aggiornamenti manuali: APK nuovo con stessa firma e `versionCode` maggiore, installato sopra il precedente.

### Alternative gratuite
- **Firebase App Distribution:** non verificata (firebase.google.com bloccato). Richiede progetto Firebase e raccoglie dati dei tester presso Google, in contrasto con "nessun dato Google" (CLAUDE §8) finche' `privacy-compliance` non lo valuta. **[verificare]** prezzi e quote.
- **F-Droid / Obtainium:** cenni, non valutati. Richiedono un repository pubblico, non adatto a una beta chiusa.

### Rischi
- Perdita della chiave: nessun aggiornamento possibile.
- Avvisi Play Protect: fiducia bassa e tester che abbandonano.
- Limite di 20 dispositivi sull'account limitato: oltre serve l'account completo (25 USD e documento).
- Dati dei tester (email, canale): trattamento di dati personali. **Parere `privacy-compliance` prima dell'invio.**
- Posizione in beta: solo "in uso", spiegazione IT/EN prima del prompt, nessun background.

## 4. Checklist prima beta (TestFlight / Play internal)
- [ ] Fondatore: account Apple Developer (solo per iOS, fuori dalla beta) e account limitato Android (§3bis); non lo creiamo noi
- [ ] Test verdi (`qa-tester`), nessun test privacy fallito
- [ ] Permesso posizione solo "in uso"; schermata di spiegazione prima del prompt di sistema (IT/EN)
- [ ] Purpose string IT/EN presenti; nessuna chiave "Always" / `ACCESS_BACKGROUND_LOCATION` nel manifest
- [ ] App usabile se l'utente nega la posizione (inserimento indirizzo)
- [ ] Consenso alla raccolta eventi con revoca semplice in-app
- [ ] `PrivacyInfo.xcprivacy` presente, manifest SDK verificati
- [ ] Target API 36 su Android
- [ ] Nessuna chiave o segreto nel bundle; firma con certificati forniti dal fondatore, fuori dal repo
- [ ] Privacy policy provvisoria IT/EN pubblicata a un URL (decisione e firma del fondatore)
- [ ] Changelog e versione semantica (es. 0.1.0+1)
- [ ] Play (solo per il lancio, non per la beta §3bis): tester chiusi e conteggio giorni **[verificare]** requisiti
- [ ] OK esplicito del fondatore prima di ogni invio

## 5. Checklist release pubblica
- [ ] Tutti i punti della beta
- [ ] Privacy policy IT/EN definitiva, firmata dal fondatore
- [ ] App Privacy (Apple) e Data safety (Google) compilate e coerenti tra loro e con la policy
- [ ] Schede store IT/EN: titolo, sottotitolo, descrizione, parole chiave, screenshot con testo
- [ ] Note per il revisore Apple: uso della posizione, nessun login, come testare
- [ ] Account demo non necessario (nessun login)
- [ ] Localizzazione completa IT/EN
- [ ] Accesso alla produzione su Play approvato **[verificare]**
- [ ] Onesta' dei numeri: nessuna accuratezza dichiarata senza misura (CLAUDE.md §1.3)
- [ ] Approvazione scritta del fondatore alla pubblicazione

## 6. Rischi aperti
- Eventi anonimi: Apple richiede comunque il consenso (5.1.1(ii)); progettare il consenso come opt-in chiaro.
- Tempi Play per account personali nuovi: possono allungare il lancio **[verificare]**.
- Policy cambiano spesso: `ops-watchdog` riverifica a ogni iterazione.
