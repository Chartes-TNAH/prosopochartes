from flask import render_template, url_for, request
#cette commande nous permet de relier nos templates à nos urls - routes
#On importe url_for pour construire des URL vers les fonctions et les pages html
from .modeles.donnees import Individu, Pays_nationalite, Occupation, Diplome, Distinction, Domaine_activite, These_enc
#cette commande nous permet de relier les classes de notre modèle de données pour pouvoir ensuite les requêter.
from sqlalchemy import and_, or_

from app.app import app
#Cette commande permet d'importer de notre package app, la variable app, qui instancie notre application.

#Les commandes suivantes nous permettent de créer différentes routes - qui correspondent à l'URL des différents pages
# de notre application :

@app.route('/')
def accueil ():
    return render_template("pages/accueil.html", title="accueil")
#la fonction render_template prend comme premier argument le chemin du template et en deuxième des arguments nommés, qui
#peuvent ensuite être réutilisé en tant que variables dans les templates.

@app.route('/chercheurs')
def chercheurs():
    """Route permettant d'afficher certains champs pour les notices de tous les chercheurs"""
    individus = Individu.query.order_by(Individu.nom.asc()).all()
#Nous stockons dans la variable individu une liste contenant les valeurs de notre table individ.
    lien = Individu.query.filter(Individu.image_lien.is_(None))
    #lien = Individu.query.filter(Individu.image_lien)
    return render_template("pages/chercheurs.html", individus=individus, lien=lien)

@app.route('/recherche_test_cc')
def recherche():
    return render_template("pages/recherche_test_cc.html")

@app.route('/resultats')
def resultats():
    """ Route permettant la recherche plein-texte
    """
    motclef = request.args.get("keyword", None)
    # Liste vide de résultat (qui restera vide par défaut si on n'a pas de mot clé)
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Résultats"
    if motclef:
        resultats = Individu.query.outerjoin(Diplome).outerjoin(Distinction).filter(
            or_(
                Individu.nom.like("%{}%".format(motclef)),
                Individu.prenom.like("%{}%".format(motclef)),
                Individu.annee_mort.like("%{}%".format(motclef)),
                Individu.annee_naissance.like("%{}%".format(motclef)),
                Individu.date_mort.like("%{}%".format(motclef)),
                Individu.date_naissance.like("%{}%".format(motclef)),
                Diplome.diplome_label.like("%{}%".format(motclef)),
                Distinction.distinction_label.like("%{}%".format(motclef))
            )
        ).order_by(Individu.nom.asc()).all()


        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/resultats.html", resultats=resultats, titre=titre)

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

@app.route('/resultats_test_cc')
def requete():

    naissanceMin = request.args.get("naissanceMin", None)
    naissanceExacte = request.args.get("naissanceExacte", None)
    naissanceMax = request.args.get("naissanceMax", None)
    mortMin = request.args.get("mortMin", None)
    mortExacte = request.args.get("mortExacte", None)
    mortMax = request.args.get("mortMax", None)
    theseMin = request.args.get("theseMin", None)
    theseExacte = request.args.get("theseExacte", None)
    theseMax = request.args.get("theseMax", None)

    requete = Individu.query

    if naissanceMin :
        requete = requete.filter(Individu.annee_naissance >= naissanceMin)
    if naissanceExacte :
        requete = requete.filter(Individu.annee_naissance == naissanceExacte)
    if naissanceMax :
        requete = requete.filter(Individu.annee_naissance <= naissanceMax)
    if mortMin :
        requete = requete.filter(Individu.annee_mort >= mortMin)
    if mortExacte :
        requete = requete.filter(Individu.annee_mort == mortExacte)
    if mortMax :
        requete = requete.filter(Individu.annee_mort <= mortMax)
    if theseMin :
        requete = requete.filter(Individu.these_enc.date_soutenance >= theseMin)
    if theseExacte :
        requete = requete.filter(Individu.these_enc.date_soutenance == theseExacte)
    if theseMax :
        requete = requete.filter(Individu.these_enc.date_soutenance <= theseMax)



    return render_template("pages/resultats_test_cc.html", requete=requete)

# LE COPIER COLLER DE LA SAUVEGARDE

    #naissanceMin = request.args.get("naissanceMin", None)
    #naissanceMax = request.args.get("naissanceMax", None)
    #naissanceExacte = request.args.get("naissanceExacte", None)
    #mortMin = request.args.get("mortMin", None)
    #mortMax = request.args.get("mortMax", None)
    #mortExacte = request.args.get("mortExacte", None)

    #query = Individu.query.filter(
    #    and_(
    #        Individu.annee_naissance.between(naissanceMin,naissanceMax),
    #        Individu.annee_mort.between(mortMin,mortMax))
    #).all()