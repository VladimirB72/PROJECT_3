# Popis projektu

Tento projekt umožňuje extrahovat výsledky voleb do Poslanecké sněmovny ČR z roku 2017 ze stránek
Českého statistického úřadu [https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ] a ukládat je.
Projekt umožňuje stahovat volební výsledky pro libovolný okres. Výsledky jsou ukládány do CSV souboru,
 který lze dále analyzovat. Uživatel zadává URL adresu požadovaného územního celku a název výstupního souboru.

## Požadavky

Python:
Ujistěte se, že máte nainstalovaný Python ve verzi 3.13 nebo novější. Verzi ověříte příkazem:
`python --version`

Virtuální prostředí:
Vytvořte virtuální prostředí pro izolaci knihoven projektu aktivujte ho:
•Windows (PowerShell):
`python -m venv .venv`
`.venv\Scripts\activate`

•macOS/Linux:
`python3 -m venv .venv`
`source .venv/bin/activate`

Instalace knihoven
Po aktivaci virtuálního prostředí nainstalujte požadované knihovny,možnost upgrade pip:
`pip install -r requirements.txt`
`python.exe -m pip install --upgrade pip`

## Spouštění projektu

Spouštění souboru *main.py* z příkazového řádku a vyžaduje dva povinné argumenty:

python main.py <odkaz_uzemniho_celku> <vysledny_soubor>

## Ukázka projektu

Výsledky hlasování pro okres Mělník:
1.argument:[https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106]
2.argument:[vysledky_melnik.csv]

Příklad spuštění pro okres Mělník:

`python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106" "vysledky_melnik.csv"`

## Ukázka průběhu

Extrahuji odkazy : <https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106>
V okrese 69 obcí.

Zpracovavam odkaz 69/69: <https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=535397&xvyber=2106>

Ukládám výsledky do souboru: vysledky_melnik.csv
Soubor "vysledky_melnik.csv" byl úspěšně uložen.
Data úspěšně uložena.
Ukončuji program.

## Výstupní soubor

| kód obce | název obce         | voliči v seznamu | vydané obálky | platné hlasy | Občanská demokratická strana |
| :------- | :----------------- | :--------------- | :------------ | :----------- | :--------------------------- |
| 534714   | Býkev              | 341              | 212           | 210          | 14                           |
| 534722   | Byšice             | 1061             | 630           | 626          | 96                           |
| 534731   | Cítov              | 923              | 575           | 569          | 52                           |
| 598291   | Čakovičky          | 461              | 321           | 320          | 64                           |
| 534749   | Čečelice           | 513              | 296           | 295          | 36                           |
| 531570   | Dobřeň             | 149              | 98            | 98           | 13                           |
| 539201   | Dolany nad Vltavou | 683              | 479           | 475          | 43                           |
| 534765   | Dolní Beřkovice    | 1154             | 644           | 642          | 92                           |

Doporučení pro práci s CSV souborem:
Otevření v Excelu:
Při otevírání CSV přímo v Excelu mohou být znaky špatně zobrazeny. Doporučuji použít funkci "Načíst data" → "Ze souboru" → "Z Text/CSV".
VCS (Visual Studio Code):
Prohlížení CSV přímo v editoru pomocí rozšíření „Excel Viewer“
