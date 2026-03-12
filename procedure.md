# Procédure de mise en place du flux RSS automatique

---

Auteur : **Jérôme Vandewalle** - Stagiaire en développement informatique

---

## Etape 1 - Configuration de l'ordinateur

Veillez à installer ```python``` ainsi que les paquets ```requests``` et ```bs4```

Installez un truc pour automatiser une tâche à certaines heures ou à certains intervalles de temps

Ex: Windows Scheduler ou Power Automate


## Etape 2 - Le fichier

Déplacez le fichier ```test.py``` sur l'ordinateur que vous choisirez pour être le responsable de la mise à jour du flux RSS

Choisissez un emplacement quelconque


## Etape 3 - Automatiser

Automatisez la tâche d'éxecuter le script python grâce à votre outil d'automatisation

Attention, veuillez ne pas le déclencher trop souvent pour éviter les requêtes répétitives sur le serveur de Vinci bien que le script soit optimisé pour vérifier si la page à changé ou non avant de mettre tout à jour (grâce à un ETag)


## Etape 4 - Exposer le fichier xml

Pour exposer le fichier sur le réseau interne, lancez un serveur python en arrière-plan avec la commande suivante:

```
python3 -m http.server 14298
```

Pour accéder au fichier XML depuis n'importe quel ordinateur connecté sur le même réseau que le responsable, vous pouvez maintenant rentrer l'ip de l'ordinateur responsable (celui sur lequel vous venez de faire la procédure) ainsi que le port et le nom du fichier :

```
http://IP_DU_PC:14298/chemin/vers/le/fichier/rss.xml
```


## Etape 5 - Utiliser le flux RSS dans Centoview

Pour utiliser le flux RSS que nous venons de mettre en place dans Centoview, ouvrez Centoview et connectez-vous. Ensuite, dans le menu latéral gauche cliquez sur ```Administration``` puis ```Les médias sociaux```.

Cliquez sur ```Créer``` en haut à gauche de votre écran puis dans le champs ```URL```, renseignez le lien vers le fichier XML.

Vous pouvez renseigner les autres champs comme bon vous semble.

Cliquez ensuite sur ```Créer``` puis votre flux RSS est maintenant utilisé dans Centoview (normalement si Centoview utilise le même réseau local que les autres machines mais ca c pas sur).

Bon après je ne sais pas comment l'inclure dans les listes, c'est une autre histoire...
