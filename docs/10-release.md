# 10 - Release e requisiti degli store

Ultima verifica: 2026-11-14 (release-manager, task T-003). Le voci **[verificare]** non sono state confermate su pagina ufficiale.
Nota: `support.google.com` non era raggiungibile dalla sessione (dominio non consentito), quindi tutte le pagine Play Console Help sono da verificare.

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
| Target API | Dal 2026-08-31 nuove app e aggiornamenti devono avere target Android 16 (API 36) o superiore. Proroga fino al 2026-11-01 (scaduta) | https://developer.android.com/google/play/requirements/target-sdk | 2026-11-14 |
| Permessi posizione (policy) | Dichiarazione dei permessi, prominent disclosure in-app prima della richiesta, video dimostrativo per background location | https://support.google.com/googleplay/android-developer/answer/9799150 | **[verificare]** (non raggiungibile) |
| Background location | Richiede `ACCESS_BACKGROUND_LOCATION`, form di dichiarazione e revisione dedicata; da evitare in beta e nella v1 | stessa pagina | **[verificare]** |
| Android 11+ | Foreground e background chiesti separatamente; il background si concede dalle impostazioni | developer.android.com (pagina target-sdk) | 2026-11-14 |
| Android 12+ | `ACCESS_COARSE_LOCATION` va richiesto sempre insieme a `ACCESS_FINE_LOCATION`; l'utente puo' concedere solo l'approssimata | idem | 2026-11-14 |
| Data safety | Compilazione obbligatoria per tutte le app, coerente con il comportamento reale e con la privacy policy | https://support.google.com/googleplay/android-developer/answer/10787469 | **[verificare]** (non raggiungibile) |
| Test per account personali nuovi | Test chiuso con un minimo di tester per un numero minimo di giorni prima di chiedere l'accesso alla produzione. Memoria: 12 tester, 14 giorni | https://support.google.com/googleplay/android-developer/answer/14151465 | **[verificare]** numeri e condizioni attuali |
| Costo account | Quota una tantum (memoria: 25 USD) e verifica d'identita' | https://support.google.com/googleplay/android-developer/answer/6112435 | **[verificare]** |

Scelta consigliata: nella v1 NON dichiarare background location (meno revisione, meno rischio). Se mai servira', aprire un task dedicato prima.

## 4. Checklist prima beta (TestFlight / Play internal)
- [ ] Fondatore ha creato account Apple Developer e Play Console (non lo facciamo noi)
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
- [ ] Play: tester chiusi reclutati e conteggio giorni avviato **[verificare]** requisiti
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
