### CV 2025

# Sergei Ivanov

---

## Lühikokkuvõte
Iseseisev ja mitmekülgne arendaja, kes on spetsialiseerunud töökindlatele ja skaleeritavatele süsteemidele. Kirglik kaasaegsete programmeerimisparadigmide ja tööriistade kasutamise vastu keeruliste probleemide lahendamisel. Omab sügavaid teadmisi full-stack arendusest, hajusüsteemidest ja CI/CD automatiseerimisest, keskendudes eelkõige suure jõudlusega keeltele nagu **Rust**.

---

## Haridus

| *Haridus* | *Algus* | *Lõpp* | *Asukoht* | *Kool*| *Staatus* |
|-------------|---------|-------|------------|---------|----------|
| Põhiharidus   | 09.2007 | 06.2016 | Narva-Jõesuu | Kool nr 5 | Lõpetatud |
| Gümnaasium | 09.2016 | 06.2019 | Narva | Gümnaasium nr 1 | Lõpetatud |
| Kõrgharidus | 09.2019 | 05.2021 | Tallinn | TalTech | Lõpetamata | 
| Bakalaureus | 09.2023 | 06.2026 | Narva | Tartu Ülikooli Narva Kolledž | Õpingud käimas | 

## Sertifikaadid
- **Foundational C# with Microsoft**  
  *Väljaandja FreeCodeCamp, 14. november 2024*  
  [Link kinnitusele](https://www.freecodecamp.org/certification/fccbe4b8c5a-8a27-493c-a983-a09fb9b9632d/foundational-c-sharp-with-microsoft)

---

## Oskused

### Programmeerimiskeeled ja raamistikud
- **Rust, Python, Kotlin, Deno, Next.js, Lua, Zig, JavaScript/TypeScript**
- **Veeb**: Next.js (Server Actions), Axum, FastAPI, Vercel
- **Andmebaasid**: PostgreSQL, SQLite, MongoDB (nõuded)
- **API-d**: REST, gRPC, WASM

### Tööriistad ja DevOps
- **Versioonihaldus**: Git, GitHub
- **Konteinerdamine**: Docker
- **CI/CD**: Kohandatud Lua skript paketi versioonihalduseks
- **Projektihaldus**: Jira, GitHub Projects

### Testimine ja kvaliteedi tagamine
- **API testimine**: Käsitsi testimine, **Postman** REST API-de jaoks.
- **Silumine ja analüüs**: **Wireshark** võrguliikluse analüüsiks, sisemine logimine ja terminali veaanalüüs.
- **Frontendi testimine**: Teadmised **Cypressist** automatiseeritud frontendi testimise jaoks.
- **Testimise metoodikad**: Kogemus üksik- ja integratsioonitestimisega.

### Arhitektuur ja süsteemidisain
- **API kommunikatsioon**: Rakendatud REST ning eksperimenteeritud gRPC ja TLS 1.3-ga turvalise suhtluse tagamiseks.
- **Mikroteenused**: Praktiseerinud teenusepõhist arhitektuuri Deno ja Rusti abil.
- **Pakendamine**: Loodud Pythoni pakett (`TestPyPIP`) ja Rusti teegi `crate` koodi taaskasutamiseks.

---

## Projektid

### 1. Suure jõudlusega API ja mikroteenuste uurimine (2025)
- **Situatsioon**: Tuvastas vajaduse luua suure jõudlusega, turvaline süsteem mikroteenuste vaheliseks suhtluseks.
- **Ülesanne**: Arendada kontseptsiooni prototüüp API-st, kasutades Rusti ja Denot, uurides erinevaid kommunikatsiooniprotokolle ja turvalist andmeedastust.
- **Tegevus**: 
  - Projekteeris ja ehitas REST API, kasutades **Denot**, ning suure jõudlusega taustaprogrammi, kasutades **Axumit (Rust)**, andmevahetuseks Server Actions kaudu.
  - Uuris ja rakendas **gRPC-d koos TLS 1.3-ga**, et tagada turvaline suhtlus Rusti kliendi ja Rusti API vahel.
  - Edukalt silus ja lahendas Deno ja gRPC/TLS seadistuse vahelised sobivuse probleemid, isoleerides probleemi ja tõestades funktsionaalsust Rusti kliendi abil.
  - Haldas tundlikke faile (`.key`, `.pem`) **`.gitignore`** abil, et säilitada turvalisus.
- **Tulemus**: Sai praktilise kogemuse arenenud protokollide (**gRPC, TLS**) ja suure jõudlusega keelte (**Rust**) kasutamisel, tõestades võimet lahendada keerukaid süsteemitasandi probleeme ja säilitada turvalisi konfiguratsioone.

### 2. Pythoni paketi CI/CD-toru (2025)
- **Situatsioon**: Vajas automatiseeritud süsteemi isikliku Pythoni paketi versioonihalduseks ja juurutamiseks.
- **Ülesanne**: Ehitada lihtne ja usaldusväärne CI/CD-toru, kasutades tuttavaid tööriistu, ilma et peaks tuginema Jenkinsi-sugustele rasketele raamistikele.
- **Tegevus**: 
  - Lõi kohandatud **Lua skripti**, mis ekstraheerib ja suurendab automaatselt paketi versiooni `__init__.py` failis.
  - Seadistas Giti toru, mis käivitatakse `release` harul, täites Lua skripti ja lükates uue versiooni reposse.
  - Praktiseeris pakettide haldust ja sõltuvuste isoleerimist, kasutades faile `requirements-dev`, `requirements-db` ja `requirements-api`.
- **Tulemus**: Automatiseeris edukalt versioonihalduse protsessi, demonstreerides CI/CD, DevOps ja skriptimise põhimõttelist mõistmist.

### 3. Full-stack veebirakenduse juurutamine (2024)
- **Situatsioon**: Tahtis luua ja juurutada full-stack rakenduse tootmiskeskkonda, integreerides erinevaid tehnoloogiaid.
- **Ülesanne**: Arendada funktsionaalne veebirakendus koos taustaprogrammiga ja juurutada see pilveteenusesse.
- **Tegevus**: 
  - Arendas veebirakenduse, kasutades **Next.js-i**, taustaprogrammi **Kotlinis** ja **Docker-konteinerit** lihtsaks juurutamiseks.
  - Juurutas konteineri AWS-i, demonstreerides võimet hallata pilveressursse.
  - Kasutas **GitHub Projects** ja Kanban-tahvlit efektiivseks projektihalduseks ja edenemise jälgimiseks.
- **Tulemus**: Juurutas edukalt töötava rakenduse, saades kriitilise kogemuse full-stack integratsioonis, Dockeris ja pilvejuurutamises, mis andis väärtuslikku tagasisidet kasutajakogemuse ja toote küpsuse kohta.

---

## Panus projektidesse

- **Mängu jõudluse analüüs**: Kasutas **OpenHardwareMonitorit** ja **Intel VTune'i** mängu jõudluse analüüsimiseks, tuvastades ja andes arendajatele tagasisidet vahemälu ja mälukasutuse probleemide kohta.
- **Panus avatud lähtekoodiga projekti**: Tuvastas ja raporteeris sobivuse probleemidest **NumPy, Pandase ja SciPyga**, tehes GitHubis koostööd probleemi lahenduse jälgimiseks.

---

## Keeleoskus

- **Vene**: Emakeel
- **Inglise**: B2 (kõne, kirjutamine) 
- **Eesti**: B2 (kõne, kirjutamine)

> *Tunnistatud ametliku eksami kaudu*