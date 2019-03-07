from flask import Flask
# import de Flask depuis la librairie flask

import os
#le module os de python nous permet d'interagir avec le système sur lequel python est en train de "tourner".

from flask_sqlalchemy import SQLAlchemy
# import de SQLAlchemy, qui nous permet de lier notre base de données à notre application, et de la requêter

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
static = os.path.join(chemin_actuel, "statics")

#Ces trois "commandes sont liées au module os, nous indiquons, quel endroit est pour nous la page de base de notre site et
#depuis cette dernière comment accéder à nos différents fichiers stockés en locals (déclarer où se trouve le dossier templates sera
#notamment très utile pour nous permettre d'afficher nos images par la suite.

app = Flask(__name__,  template_folder=templates, static_folder=static

            )
#Instanciation de notre application, nous lui ajoutons deux arguments qui permettent de faire le lien
#vers nos dossiers déclarés via les commandes os.

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../prosopochartes.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG'] = True
# Initiation de l'extension
db = SQLAlchemy(app)

#Selon le manuel de Grinberg, _name_ est une variable Python prédéfinie qui prend le nom du module dans lequel elle est
#utilisée. Nous avions vu en cours qu'il pouvait être judicieux de lui donner un nom distinct dans le cas du développement
#de plusieurs applications tournant sur le même serveur. Comme dans notre cas nous en développons une, nous choisissons de
#suivre les préconisations de Grinberg.

# app est ici une variable définie comme appartenant à la classe Flask, à ne pas confondre avec notre package app (initialisé
#avec notre fichier __init__.py.) et qui contient notre application.

from app import routes

#Cette commande permet de relier nos routes - urls à notre application. Elle se situe en dernier car routes a besoin de
# notre variable app pour fonctionner. Ceci permet d'éviter des erreurs de code.
