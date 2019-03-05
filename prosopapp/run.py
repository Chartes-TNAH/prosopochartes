from app import app

#Ce script permet de déclarer notre application Flask. Littéralement on lui dit d'importer notre variable
#app qui correspond à notre application, de notre package app (cette variable est définie dans le fichier app.py.

# --------Flaskenv------------#
#Selon le tutoriel de Grinbert afin de pouvoir afficher notre application en local, nous devons spécifier à Flask comment
#l'importer. Ceci se fait via la commande : export FLASK_APP=run.py avant de pouvoir l'afficher en mode local via :
#flask run.
#Depuis  la version 1.0 Flask autorise a mémoriser la première commande de déclaration. Cela se fait via la création d'un
#fichier placé au plus haut de notre projet, c'est le fichier .flaskenv. Il nécessite au préalable l'installation du package
#python python-dotenv.
#Ceci est l'équivalent de ce que nous avions vu en cours via la commande python run.py, c'est pourquoi même si le procédé est
#différent, nous l'avons appelé run.py