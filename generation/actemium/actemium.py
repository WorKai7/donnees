import requests
import os
import re
from bs4 import BeautifulSoup

# Import grâce au package utils
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from utils.start_xml_file import start_file
from utils.end_xml_file import end_file
from utils.write_xml import write_xml

os.chdir(os.path.dirname(__file__))


# Connexion au site
base_url = "https://www.actemium.fr/realisations-evenements/"


def scrap_description(url: str):
    print("Scrapping", url)
    article_response = requests.get(url)
    article_response.raise_for_status()

    soup = BeautifulSoup(article_response.text, "html.parser")

    return soup.find("p").get_text(strip=True)



print("\n\nScrapping", base_url, "\n\n")

response = requests.get(base_url)
response.raise_for_status()

# Instanciation de soup
soup = BeautifulSoup(response.text, "html.parser")

articles = []

images_divs = soup.find_all("div", class_="image")
dates = soup.find_all("time", class_="date")
titres = soup.find_all("h3", class_="title")
links = soup.find_all("a", class_="link-minimal-arrow")


for i in range(len(images_divs)):
    article = {}

    link = links[i].get("href")

    article["Titre"] = titres[i].get_text(strip=True)
    article["Date"] = dates[i].get_text(strip=True)
    article["Image"] = images_divs[i].get("data-bg")
    article["Lien"] = link
    article["Description"] = scrap_description(link)


    articles.append(article)


# Ecriture

start_file(
    "actemium/actu.rss",
    "Flux RSS actualités Actemium",
    "https://workai7.github.io/auto-rss/rss/actemium/actu.rss",
    "Flux RSS contenant les informations sur les actualités du site d'Actemium, généré par un script de scrapping"
)

for article in articles:
    write_xml(
        "actemium/actu.rss",
        article["Titre"],
        article["Description"],
        article["Image"],
        article["Lien"],
        article["Date"]
    )

end_file("actemium/actu.rss")


print("\nDone\n")