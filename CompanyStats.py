from dataclasses import dataclass
from bs4 import BeautifulSoup
import re

@dataclass
class Company:
    ticket: str
    price: float = None
    pe: float = None

class CompanyStats:
    findTag = {
        2022: {
            "company_div": ("tr", "row-iVZpYhgj listRow"),
            "ticket": ("a", "apply-common-tooltip tickerName-absbzmSX"),
            "columns": ("td", "cell-s_9Ijkac right-s_9Ijkac"),
            "priceIdx": 0,
            "peIdx": lambda columns: 6 if len(columns) == 9 else 4
        },

        2024: {
            "company_div": ("tr", "row-RdUXZpkv listRow"),
            "ticket": ("a", "apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"),
            "columns": ("td", "cell-RLhfr_y4 right-RLhfr_y4"),
            "priceIdx": 0,
            "peIdx": lambda columns: 5
        }
    }
    
    def __init__(self, filename: str, year: int):
        with open(filename) as file:
            searchTags = CompanyStats.findTag[year]
            soup: BeautifulSoup = BeautifulSoup(file, "html.parser")
            companies = soup.find_all(searchTags["company_div"][0], attrs={"class": searchTags["company_div"][1]})
            self.stats = {}
            for company in companies:
                ticket = company.find(searchTags["ticket"][0], attrs={"class": searchTags["ticket"][1]}).text

                columns = company.find_all(searchTags["columns"][0], attrs={"class": searchTags["columns"][1]})

                priceIdx = searchTags["priceIdx"]
                peIdx = searchTags["peIdx"](columns)

                if len(columns) == 0: continue

                price = float(re.findall("\\d+\\.\\d+", columns[priceIdx].text)[0]) # Do not care about currency
                pe = float(columns[peIdx].text) if columns[peIdx].text != "—" else None

                self.stats[ticket] = Company(ticket, price, pe)

    def getStats(self) -> dict:
        return self.stats

