# datascience-ybettayeb
Classifieur de spam

Le cahier des charges complet se trouve dans le dépot. 
Le classeur .ipynb qui détaille mon raisonnement et cheminement se trouve dans le dépot.
Les différents scripts utilisés sont placés dans le répértoire scripts

# Fonctionnalités 
- Classifieur de messages qui permets de detecter les messages dits "Spam" des autres messages
- API, disponible dans le fichier app.py qui permets de monter un serveur flask et expose des fonctions notament une fonction permettant d'envoyer un message et d'obtenir une prédiction
sur la nature du message. 
- Une base de données Sqlite3 qui va stocker les messages envoyés à l'api avec un historique des prédictions.
- Une doc générée avec Pdoc.
- Un notebook jupyter détaillant le model, mon raisonnement et quelques metriques de performance du modele. 


# Guide d'utilisation 
Il faut d'abord installer les différentes libraries
``` pip3 install requirements.txt ```

puis entrainer et sauvegarder le modele : 
``` python3 ./script/model.py ``` 
Ce script va créer le modele et l'entrainer sur le fichier spam.csv qui se trouve dans le répértoire "Data".
Il est aussi possible de passer votre propre jeu de données en parametres comme suit : 
``` python3 ./script/model.py Chemin/VersMon/SuperDataSet.csv ```

une fois le modele entrainé il sera enregistré dans le répértoire ```models```
Il faut maintenant initialiser la base de données comme suit : ``` python3 script/initDb.py```

Pour démarrer l'api : ```python3 ./api/app.py```
Celà va démarrer le serveur flask.
Une fois le serveur en ligne voici le guide des requetes

Pour prédire si un message est un spam ou non : 
```127.0.0.1:5000/api/v1/resources/predictions/predict?Message="MonSuperMessage"```
l'api vous retournera alors un résultat avec le message, la prédiction 1 si spam 0 sinon, et la confiance du modele dans la prédiction
le message est alors enregistré dans la base de données, avec l'IP de son auteur
```127.0.0.1:5000/api/v1/resources/predictions/predict/spams``` 
vous retournera tout les messages classés en tant que "Spams"

```/api/v1/resources/predictions/all``` vous retournera l'entièreté des messages envoyés à l'API avec leur classification.


# To Do : 
1. entrainement du modele avec les prédictions effectuées (Aucune idée du workflow, dump en csv de la bd, marquage manuel des faux positifs, entrainement) 
2. ~~Possible amélioration du modele avec une liste de "mauvais sujets" et un compteur de digits dans les messages ?~~
3. Tests d'intégrité du chemin sur le script d'entrainement du modele et d'autres tests de ce genre à travers le fichier et l'app... 
4. Peut etre une UI et une appweb pour flagger manuellement les faux positifs/faux négatifs


