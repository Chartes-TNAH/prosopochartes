from flask import render_template, url_for, request
#cette commande nous permet de relier nos templates à nos urls - routes
#On importe url_for pour construire des URL vers les fonctions et les pages html
from .modeles.donnees import Individu, Pays_nationalite, Occupation, Diplome, Distinction, Domaine_activite, These_enc
#cette commande nous permet de relier les classes de notre modèle de données pour pouvoir ensuite les requêter.


from app.app import app
#Cette commande permet d'importer de notre package app, la variable app, qui instancie notre application.

from sqlalchemy import and_, or_

#Les commandes suivantes nous permettent de créer différentes routes - qui correspondent à l'URL des différents pages
# de notre application :

@app.route('/')
def accueil ():
    return render_template("pages/accueil.html", title="accueil")
#la fonction render_template prend comme premier argument le chemin du template et en deuxième des arguments nommés, qui
#peuvent ensuite être réutilisé en tant que variables dans les templates.

@app.route('/chercheurs')
def chercheurs():
    individus = Individu.query.order_by(Individu.annee_naissance.asc()).all()
    return render_template("pages/chercheurs.html", individus=individus)

@app.route('/recherche_test_cc')
def recherche():
    return render_template("pages/recherche_test_cc.html")

@app.route('/resultats_test_cc')
def query():

    naissanceMin = request.args.get("naissanceMin", None)
    naissanceMax = request.args.get("naissanceMax", None)
    naissanceExacte = request.args.get("naissanceExacte", None)
    mortMin = request.args.get("mortMin", None)
    mortMax = request.args.get("mortMax", None)
    mortExacte = request.args.get("mortExacte", None)

    query = Individu.query.filter(
        and_(
            Individu.annee_naissance.between(naissanceMin,naissanceMax),
            Individu.annee_mort.between(mortMin,mortMax))
        and_(Individu.annee_naissance==naissanceExacte,
            Individu.annee_mort==mortExacte)
    ).order_by(Individu.annee_naissance.asc()).all()



    return render_template("pages/resultats_test_cc.html", query=query)


#cette route correspond à la page qui affichera les notices abrégées des résultats
# à voir si on choisit de la conserver sous la dénomination résultat où si l'on préfère un nom qui reprend les mots-clés?

@app.route('/noticechercheur/<int:individu_id>')
def noticechercheur(individu_id):
    """"Route permettant l'affichage de la notice d'un chercheur
    :param individu_id : Identifiant numérique du chercheur
    """
    unique_individu = Individu.query.get(id)
    return render_template("pages/noticechercheur.html", individu = unique_individu)
#idealement nomchercheur est remplacé par le nomprenom du chercheur
#cette page correspond à la notice complète sur le chercheur
#<string:nomchercheur>
