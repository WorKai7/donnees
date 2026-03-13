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
base_url = "https://www.vinci-energies.com/actualites/"


def scrap_description(url: str):
    print("Scrapping", url)
    article_response = requests.get(url)
    article_response.raise_for_status()

    soup = BeautifulSoup(article_response.text, "html.parser")

    return soup.find("p", class_="text").get_text(strip=True)



print("\n\nScrapping", base_url, "\n\n")

response = requests.get(base_url)
response.raise_for_status()

# Instanciation de soup
soup = BeautifulSoup(response.text, "html.parser")

articles = []

articles_divs = soup.find_all("div", class_="featured-image")
dates = soup.find_all("time", class_="date")
titres = [titre for titre in soup.find_all("h4", class_="title") if not titre.find_parent("div", class_="content")]
links = soup.find_all("a", class_="intern-link")


for i in range(len(articles_divs)):
    article = {}

    img_style = articles_divs[i].get("style")
    url_search = re.search(r"url\((.*?)\)", img_style)

    if url_search:
        image = url_search.group(1).strip('\'"')

    link = links[i].get("href")

    article["Titre"] = titres[i].get_text(strip=True)
    article["Date"] = dates[i].get_text(strip=True)
    article["Image"] = image
    article["Lien"] = link
    article["Description"] = scrap_description(link)


    articles.append(article)


# Ecriture

start_file(
    "vinci-energies/actu.rss",
    "Flux RSS actualités Vinci Energies",
    "https://workai7.github.io/auto-rss/rss/vinci-energies/actu.rss",
    "Flux RSS contenant les informations sur les actualités du site de Vinci Energies, généré par un script de scrapping"
)

for article in articles:
    write_xml(
        "vinci-energies/actu.rss",
        article["Titre"],
        article["Description"],
        article["Image"],
        article["Lien"],
        article["Date"]
    )

end_file("vinci-energies/actu.rss")


print("\nDone\n")