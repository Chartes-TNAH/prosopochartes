from flask import Flask


#import de Flask depuis la librairie flask


app = Flask(__name__
            )

#Selon le manuel de Grinberg, _name_ est une variable Python prédéfinie qui prend le nom du module dans lequel elle est
#utilisée. Nous avions vu en cours qu'il pouvait être judicieux de lui donner un nom distinct dans le cas du développement
#de plusieurs applications tournant sur le même serveur. Comme dans notre cas nous en développons une, nous choisissons de
#suivre les préconisations de Grinberg.

# app est ici une variable définie comme appartenant à la classe Flask, à ne pas confondre avec notre package app (initialisé
#avec notre fichier __init__.py.) et qui contient notre application.

from app import routes

#Cette commande permet de relier nos routes - urls à notre application. Elle se situe en dernier car routes a besoin de
# notre variable app pour fonctionner. Ceci permet d'éviter des erreurs de code.
