from flask import render_template
#cette commande nous permet de relier nos templates à nos urls - routes.

from app.app import app
#Cette commande permet d'importer de notre package app, la variable app, qui instancie notre application.

#Les commandes suivantes nous permettent de créer différentes routes - qui correspondent à l'URL des différents pages
# de notre application :
@app.route('/')
@app.route('/accueil')
def accueil ():
    return render_template("templates/pages/accueil.html")
#la fonction render_template prend comme premier argument le chemin du template et en deuxième des arguments nommés, qui
#peuvent ensuite être réutilisé en tant que variables dans les templates.

@app.route('/chercheurs')
def chercheurs():
    return render_template("templates/pages/chercheurs.html")

@app.route('/recherche')
def recherche():
    return render_template("templates/pages/recherche.html")

@app.route('/resultats')
def resultat():
    return render_template("templates/pages/resultats.html")
#cette route correspond à la page qui affichera les notices abrégées des résultats
# à voir si on choisit de la conserver sous la dénomination résultat où si l'on préfère un nom qui reprend les mots-clés?
@app.route('/<string:nomchercheur>')
def nomchercheur():
    return render_template("templates/pages/accueil.html")
#idealement nomchercheur est remplacé par le nomprenom du chercheur
#cette page correspond à la notice complète sur le chercheur
