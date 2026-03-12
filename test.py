import requests
import os
from bs4 import BeautifulSoup

os.chdir(os.path.dirname(__file__))

# Fonction utile pour échapper aux caractères spéciaux
def escape_xml(text):
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )


# Connexion au site
base_url = "https://www.vinci.com"

# URL spécifique pour les communiques de presse : https://www.vinci.com/newsroom?f[0]=newsroom_content_type:communique
#                                 Pour les actu : https://www.vinci.com/newsroom?f[0]=newsroom_content_type:actu

response = requests.get(base_url + "/newsroom")

# Instanciation de soup
soup = BeautifulSoup(response.text, "html.parser")


# Recherche des divs qu'on a besoin
articles_divs = soup.find_all("article", class_="pr-teaser")
titres = soup.find_all(class_="pr-teaser__title")
images_divs = soup.find_all("div", class_="pr-teaser__image")
details_divs = soup.find_all("div", class_="pr-teaser__details")

articles = []

# Boucle sur chaque articles trouvé
for i in range(len(titres)):
    article = {}

    # Récupération des informations nécessaires
    article_link = [child for child in articles_divs[i].children if child.name][0].get("href")
    image = images_divs[i].find("img")
    enfants = [child for child in details_divs[i].children if child.name]
    categorie = enfants[0]
    date = enfants[-1]


    # Gestion du pays
    if len(enfants) == 3:
        pays = enfants[1]
        article["Pays"] = pays.get_text(strip=True)
    else:
        article["Pays"] = "Non spécifié"


    # Alimentation du dictionnaire avec les données trouvées
    article["Titre"] = titres[i].get_text(strip=True)
    article["Image"] = base_url + image.get("src")
    article["Categorie"] = categorie.get_text(strip=True)
    article["Date"] = date.get_text(strip=True)
    article["Lien"] = base_url + article_link


    articles.append(article)


# Affichage
# for article in articles:
#     print("--------------------------------\n")
#     print("Titre :", article["Titre"])
#     print("Image :", article["Image"])
#     print("Categorie :", article["Categorie"])
#     print("Date :", article["Date"])
#     print("Pays :", article["Pays"])
#     print("Lien :", article["Lien"], "\n")



# Ecriture dans un fichier XML pour générer un flux RSS
with open("vinci.rss", "w", encoding="utf-8") as rss:
    # En tête
    rss.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    rss.write('<rss version="2.0">\n')
    rss.write('    <channel>\n')
    rss.write('        <title>Flux RSS infos VINCI</title>\n')
    rss.write('        <link>file:///c%3A/Users/jerome.vandewalle/Documents/tests/vinci.rss</link>\n')
    rss.write('        <description>Flux RSS contenant les informations du site de VINCI, généré par un script de scrapping</description>\n')

    # Boucle sur les articles
    for article in articles:
        rss.write('\n        <item>\n')
        rss.write(f'            <title>{escape_xml(article["Titre"])}</title>\n')
        rss.write(f'            <link>{escape_xml(article["Lien"])}</link>\n')

        # Description avec la catégorie et le pays
        if article["Pays"] == "Non spécifié":
            description = escape_xml(article["Categorie"])
        else:
            description = escape_xml(article["Categorie"]) + "-" + escape_xml(article["Pays"])

        rss.write(f'            <description>{description}</description>\n')
        rss.write(f'            <pubDate>{escape_xml(article["Date"])}</pubDate>\n')
        rss.write(f'            <enclosure url="{escape_xml(article["Image"])}" type="image/jpeg" />\n')
        rss.write('        </item>\n')


    # Fermeture des balises
    rss.write('\n    </channel>\n')
    rss.write('</rss>\n')


print("Fichier généré")