"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Vladimír Bořek
email: borek.vladimir@iex.cz
"""

import os
import sys
import csv
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def extract_urls(main_page_url):
    """Extrahuje URL adresy z hlavní stránky.
    Vstup: URL hlavní stránky
    Výstup: Seznam extrahovaných URL adres
    Zpracování chyb: Vyvolá ConnectionError při problémech s připojením,
     ValueError při neexistující cestě
    """
    try:
        page = requests.get(main_page_url, timeout=10)
        page.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Chyba při připojení k serveru: {e}") from e

    soup = BeautifulSoup(page.content.decode(page.encoding), "html.parser")
    if soup.title and soup.title.text.lower() == "404 not found":
        raise ValueError("Zadaná cesta na serveru neexistuje")

    links_all = soup.find_all("a")
    links_extracted = [
        lnk.get("href") for lnk in links_all if lnk.text.isnumeric() and lnk.get("href")
    ]

    return links_extracted


def get_base_url(url_string):
    """Získá základní URL adresu z dané URL.
    Vstup: URL řetězec
    Výstup: Základní URL adresa"""

    url_fields = url_string.split("/")
    del url_fields[-1]
    base_url = "/".join(url_fields) + "/"
    return base_url


def extract_general_stats(soup):
    """Extrahuje obecné statistiky o obci z HTML stránky.
    Objekt BeautifulSoup reprezentující HTML podstránky obce.
    Výstup: Slovník obsahující:název obce, počet voličů v seznamu,
    počet vydaných obálek, počet platných hlasů."""

    general_stats = {
        "název obce": " ".join(
            soup.find("h3", string=lambda t: "Obec:" in t).text.strip().split(" ")[1:]
        ),
        "voliči v seznamu": int(
            soup.find("td", headers="sa2").text.replace("\xa0", "")
        ),
        "vydané obálky": int(soup.find("td", headers="sa3").text.replace("\xa0", "")),
        "platné hlasy": int(soup.find("td", headers="sa6").text.replace("\xa0", "")),
    }
    return general_stats


def extract_party_data(soup):
    """Extrahuje data o politických stranách a jejich počtu hlasů.
    Vstup: Objekt BeautifulSoup reprezentující HTML podstránky obce.
    Výstup: Slovník, kde klíče jsou názvy stran a hodnoty jsou počty hlasů."""

    def get_data(headers):
        cells = [
            td.get_text(strip=True)
            for td in soup.find_all("td", headers=headers)
            if td.get_text(strip=True) != "-"
        ]
        return cells

    party_names = get_data("t1sa1 t1sb2") + get_data("t2sa1 t2sb2")

    vote_cells = [
        td
        for td in soup.find_all("td", headers="t1sa2 t1sb3")
        + soup.find_all("td", headers="t2sa2 t2sb3")
        if td.get_text(strip=True) != "-"
    ]
    party_votes = [
        int(td.get_text(strip=True).replace("\xa0", "")) for td in vote_cells
    ]

    return dict(zip(party_names, party_votes))


def get_stats(sub_page_url):
    """Získá všechny statistiky (obecné i stranické) pro konkrétní obec.
    Vstup: URL podstránky obce.
    Výstup: Slovník kombinující obecné statistiky a data o stranách."""

    stats = {}
    try:
        for param in sub_page_url.split("?")[1].split("&"):
            if "xobec" in param:
                stats["kód obce"] = int(param.split("=")[1].strip())

        page = requests.get(sub_page_url, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.content.decode(page.encoding), "html.parser")

        if soup.title.text.lower() == "404 not found":
            raise ValueError("Zadaná cesta na serveru neexistuje")

        stats.update(extract_general_stats(soup))
        stats.update(extract_party_data(soup))

    except requests.RequestException as e:
        raise ConnectionError(f"Chyba při připojení k serveru: {e}") from e
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Chyba při zpracování dat: {e}") from e

    return stats


def scrape_elections_data(input_url):
    """Extrahuje volební data z dané URL.
    Vstup: Vstupní URL
    Výstup: Seznam výsledků"""

    url_base = get_base_url(input_url)
    print(f"Extrahuji odkazy : {input_url}")
    url_list = extract_urls(input_url)

    if not url_list:
        exit("Ukončuji program")
    else:
        print(f"V okrese {len(url_list)} obcí.\n")

    results = []
    for index, relative_url in enumerate(url_list, start=1):
        full_url = url_base + relative_url
        print(f"\rZpracovavam odkaz {index}/{len(url_list)}: {full_url}", end="")
        results.append(get_stats(full_url))
    print("\n")
    return results


def save_csv_file(output_file_name, results_list):
    """Uloží výsledky do CSV souboru.
    Vstupy: Název výstupního souboru, seznam výsledků
    Zpracování chyb: Ošetřuje IOError a ImportError"""

    try:

        if os.path.exists(output_file_name):
            print(f'Soubor "{output_file_name}" již existuje a bude přepsán.')

        with open(output_file_name, mode="w", newline="", encoding="utf-8") as csv_file:
            print(f"Ukládám výsledky do souboru: {output_file_name}")
            field_names = results_list[0].keys()
            writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=field_names)
            writer.writeheader()
            for list_itm in results_list:
                writer.writerow(list_itm)
        print(f'Soubor "{output_file_name}" byl úspěšně uložen.')
    except IOError as e:
        print(f'Chyba při zápisu do souboru "{output_file_name}": {str(e)}')
        exit("Ukončuji program.")
    except ImportError:
        print(f'Neočekávaná chyba při ukládání souboru "{output_file_name}": {str(e)}')
        exit("Ukončuji program.")


def validate_url(url_in):
    """Ověří platnost vstupní URL.
    Vstup: URL adresa
    Výstup: True pokud je URL platná
    Zpracování chyb: Vyvolá ValueError při neplatné URL"""

    result = urlparse(url_in)

    if not all([result.scheme, result.netloc]):
        raise ValueError("Neplatný formát URL")

    if (
        not result.netloc.endswith("volby.cz")
        or "/pls/ps2017nss/ps32" not in result.path
    ):
        raise ValueError(
            "URL musí směřovat na volební výsledky 2017.\n"
            "Např: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106"
        )

    return True


def main():
    """Hlavní funkce programu.
    Zpracovává argumenty příkazové řádky
    Volá ostatní funkce pro extrakci a ukládání dat
    Zpracování chyb: Ošetřuje ValueError, RequestException a ImportError"""

    try:
        args = sys.argv[1:]
        if len(args) != 2:
            raise ValueError(
                "Chybný počet argumentů. Použijte: python main.py <URL> <výstupní_soubor>"
            )

        url_in, file_out = args
        validate_url(url_in)
        res_list = scrape_elections_data(url_in)
        save_csv_file(file_out, res_list)
        print("Data úspěšně uložena.")

    except ValueError as e:
        print(f"Chyba: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Chyba při zpracování URL: {e}")
    except ImportError:
        print("Neočekávaná chyba:Zkontroluj URL")
    finally:
        print("Ukončuji program.")
        sys.exit(1)


if __name__ == "__main__":
    main()
