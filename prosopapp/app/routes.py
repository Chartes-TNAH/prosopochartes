from flask import render_template
from app import app

@app.route('/')
@app.route('/accueil')
def accueil ():
    return render_template("templates/pages/accueil.html")

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
@app.route('/<int:nomchercheur>')
def nomchercheur():
    return render_template("templates/pages/accueil.html")
#idealement nomchercheur est remplacé par le nomprenom du chercheur
#cette page correspond à la notice complète sur le chercheur
