---
bibliography: references.bib
geometry:
  - a4paper
  - left=3cm
  - right=2cm
  - top=2.5cm
  - bottom=2.5cm
linestretch: 1.5
header-includes:
  - \usepackage{float}
  - \usepackage{titlesec}
  - |
    \titleformat{\section}{\fontsize{14pt}{17pt}\selectfont\bfseries\uppercase}{\thesection.}{1em}{}
    \titlespacing*{\section}{0pt}{12pt}{20pt}
    \titleformat{\subsection}{\fontsize{12pt}{15pt}\selectfont\bfseries}{\thesubsection.}{1em}{}
    \titlespacing*{\subsection}{0pt}{12pt}{12pt}
    \titleformat{\subsubsection}{\fontsize{12pt}{15pt}\selectfont\bfseries}{\thesubsubsection.}{1em}{}
    \titlespacing*{\subsubsection}{0pt}{12pt}{12pt}
  - \usepackage{graphicx}
  - \usepackage{times}

  - \usepackage{inconsolata} 
  - \usepackage{soul}
  - \DeclareTextFontCommand{\texttt}{\ttfamily\small}

  - \usepackage[singlelinecheck=false]{caption}
  - |
    \captionsetup[table]{position=above, justification=raggedright}
    \captionsetup[figure]{position=below, justification=raggedright}


---

# SISSEJUHATUS { - }

Ülesanne kirjeldus on

Nädal 17: Lõputöö - essee ja tagasiside (Tähtaeg: 10. juuni)

Kirjutage digipöördest oma erialases valdkonnas - millised digitaalsed lahendused on praegu kasutuses, millised on kohe tulemas või milliseid oleks hädasti vaja. Samuti visioon, milline on teie oma erialane valdkond ca 10 aasta perspektiivis.

Teine osa: tagasiside ainele kui tervikule, ca 1 lk mahus. Võib käsitleda ka konkreetseid teemasid, kuid peamine fookus peaks olema tervikul.

## Essee

Mina kirjutan nii endast kui ka IT sektorist. Mida ma teen IT-s? Miks see on kursus oli kasulik? Esiteks, mina õpisin mitu programmerimist keelt ja raamistikku. Näiteks, enne 2025, mina kasutasin palju JavaScript-i kasutades NextJS (React) raamistikku. Mina kasutasin neid tööristaid nii front-endi kui ka back-endi jaoks. Pärast 2025 mina hakkasin Rust kasutama. Miks ja milleks? See on väga keeruline küsimus, sest mina katsetasin mitu keelt ja tehnoloogiat IT-s ja mulle meeldis Rust kasutamine. See tundub nii, et mul on süsteem-mõtte käik. Rust on süsteemikeel, mis võimaldab mul kirjutada kiiret ja tõhusat koodi, samas kui see pakub ka turvalisust ja mälu haldamise kontrolli. See on eriti kasulik, kui ma töötan projektidega, mis nõuavad kõrget jõudlust või madalat taset juurdepääsu riistvarale. Lisaks on Rustil tugev kogukond ja palju raamistikke, mis muudavad arendamise lihtsamaks ja nauditavamaks.  

Lõputöö kirjutamisel pidin mina vastama küsimusele: mis on minu DSA Kuuking tekist kasu? Vastus on aga lihtne: 2026 aastal on Python-il palju tekke, mille hulgas on pahavara [@cve_2026_42271]. See tähendab, et tänapäeval ei saa usalda PIP-süsteemi [@litellm_pypi_compromise_2026]. Me peame mõtlema, mida me vajame ja miks, et vähendada meie project arendamiseks kasutatavaid tekke. See ei sõltu programmerimiskeelest, vaid sellest, kuidas tarkvara arendaja läheneb probleemi lahendamisele; kuidas ta kasutab olemasolevaid varasid. 

Teine aspekt on selles, et kassaaegsel maailmas arutletatakse, kas mälu või kiiruse optimeerimine on olulisem. Seepärast inimesi kasutab mitu keelt antud projekti arendamisel. Näiteks, veebis kasutatakse JS ja Golang ehk Go [@theprimeagen_why_go_2024]. Vanilla JS-st ei piisa tänapäeval, sest JS ei halda vigu. Pythonis on sama probleem: Pythoni programmi arendamisel viga tekkimise tõenäosus on suhteliselt suur. Näidena toon TypeScript-i funktsiooni:

```ts
async function fetchData(request: NextRequest, response: NextResponse) {
  try {
    const data = await fetch('https://api.example.com/data');
    const jsonData = await data.json();
    return new NextResponse(JSON.stringify(jsonData), { status: 200 });
  } catch (error) {
    console.error('Error fetching data:', error);
    return new NextResponse('Error fetching data', { status: 500 });
  }
}
```

Lugeja saab endalt küsida, kus on vead? Try-Catch-ist vaatamata pole siin vigu. Need puuduvad ja see kood on väga levinud. Iga Junior arendaja kirjutab seda nende React äppis. Teine näide on, et

```py
class DoublyLinkedList[T](LinkedList):
    def __init__(self) -> None:
        super().__init__()
        self._tail: Optional[Node[T]] = None
        self._type: int = 1 
```

Kui `self._type` ei kasutataks, siis tekkib olukord, kus kasutaja kasutab `dll.add_to_end`, see hakkab kasutama `DoublyLinkedListNode` asemel `SinglyLinkedListNode`. Kui ei mõtle Pythonis, siis need vead tekivad ja kui koodibaas kasvab, siis see saab raskemaks, et hallata kõik vigu. Nõnda kasutusele võetakse teisi keeli tänapäeval [@rust_python_symbiosis_2015]. 

Vibe-koodimine on väga probleematiline ja selle probleem on väga kassaegne [@vibe_coding_security_2026]. See on väga levinud, et arendajad kirjutavad koodi, mis töötab, aga see ei ole hästi struktureeritud ega hooldatav. See võib viia tehnilise võlani, kus koodibaas muutub keeruliseks ja raskesti hallatavaks. Selle vältimiseks on oluline järgida parimaid tavasid ja kasutada keeli, mis pakuvad tugevat tüüpsüsteemi ja muid tööriistu, mis aitavad vältida vigu. Rust on üks selline keel, mis pakub tugevat tüüpsüsteemi ja muid tööriistu, mis aitavad vältida vigu ja parandada koodi kvaliteeti.

Tänapäeval on teada, et cURL keeldus Anthropic Claude AI-lt päringute tegemast, kuna see oli tuvastanud, et päringud olid seotud pahavaraga [@lobsters_curl_ai_2026]. See on näide sellest, kuidas pahavara võib mõjutada meie digitaalseid lahendusi ja miks on oluline olla teadlik turvariskidest ning kasutada turvalisi ja usaldusväärseid tööriistu [@theprimetime_mythos_2026]. 

Viimaseks, saan rääkida tulevikust. Täna saab näha ja teada saada, et IT valdkonnas on paljud probleemid:

- Junior arendajate arv kahenes
- Senior-id on juba hõivatud; näiteks, pole nii palju Rust arendajaid
- AI oli väga hea, kuid tänapäeval enamik vältib AI kasutamist (unenäod on tõelised probleemid)
- On palju "legacy" koodi, mida peab teadma ja kindlustama, et see töötaks tulevikus ka
- AI vaib-koodist tingitud on äritegevuse hulk suurenenud: on raske luua midagi uut ja seetõttu firmad vallandavad nende töötajaid.

Nii räägitakse, et IT hakka ennast paika panema uuesti, nullist, kuna ei ole inimesi, kes teavad, kuidas tarkvara arendatakse. Enamik oskab vibe-koodi kirjutada, ega ei saa need tarkvaratehnika tunda. Praegu saab nentida, et AI pole usaldusväärne. See saab välja mõelda mitte-eksisteerivaid teabeallikaid. Inimesi unistab ilusast maailmast, kuid Claude ütleb neil, et peetakse kaht tuhat eurot maksma, mis saadab neile äratuse sõnumit. Sellepärast võib ennustada, et 10 aasta pärast AI saab konstulandiks, mitte inseneriks. Inseneriks jääb inimene.

## Tagasiside

Tervikuna on see kursus väga tähtis, sest see aitab tugengitel ennast kontrollida. Näiteks mina keskendusin Rust-li, mistõttu mina ei pandud tähelepanu üldteabele. Mina võin unustada midagi. See kursus tuletab meelde asju, mida võidi unustada. Näidena saab tooma seda, et kursuse jooksul sain harjutada bit-i kasutamist. Selleks mina kasutan Rust:

```rs
fn main() {
    let number = 42;
    // :b prints binary
    // :08b prints binary padded with zeros to 8 places
    println!("Number: {}", number);
    println!("Bits: {:b}", number);   
    println!("Bits (padded): {:08b}", number); 

    // 1. Literal approach
    let bits_literal = 0b00101010; 
    println!("Literal 0b00101010 is: {}", bits_literal);

    // 2. String parsing approach
    let bit_string = "101010";
    let parsed_number = u32::from_str_radix(bit_string, 2).unwrap();
    
    println!("Parsed string '{}' is: {}", bit_string, parsed_number);


    let val: u8 = 0b00001000; // Only the 3rd bit (index starting at 0) is set
    
    // Check if the 3rd bit is set using a mask
    let mask = 1 << 3; 
    if (val & mask) != 0 {
        println!("The 3rd bit is active!");
    }
}
```

Neid kasutati, et lahendada `01. Bitt ja bait, kahendloogika, arvuti tööpõhimõte` ülesande. Nõnda mulle meeldis, see kursus.

## KOKKUVÕTTE

Kõkkuvõttes, see kursus on väga kasulik, sest see aitab arendajatel mõista ja kasutada erinevaid programmeerimiskeeli ja -raamistikke, mis on olulised tänapäeva IT-tööstuses. See annab võimaluse õppida nii Pythonit kui ka Rustit, mis on kaks väga erinevat keelt, kuid mõlemad pakuvad unikaalseid eeliseid ja võimalusi. Kursus aitab arendajatel mõista, kuidas valida õige tööriista õige ülesande jaoks ning kuidas kasutada neid tööriistu tõhusalt ja turvaliselt. Lisaks annab see kursus võimaluse harjutada ja rakendada oma teadmisi praktilistes projektides, mis on oluline osa õppimisprotsessist. Kokkuvõttes on see kursus suurepärane võimalus arendajatele laiendada oma oskusi ja teadmisi ning valmistuda tulevikuks IT-tööstuses.

## REFERENCES

::: {#refs}
:::