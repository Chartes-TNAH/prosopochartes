from flask import render_template, url_for, request
#cette commande nous permet de relier nos templates à nos urls - routes
#On importe url_for pour construire des URL vers les fonctions et les pages html
from .modeles.donnees import Individu, Pays_nationalite, Occupation, Diplome, Distinction, Domaine_activite, These_enc
#cette commande nous permet de relier les classes de notre modèle de données pour pouvoir ensuite les requêter.
from sqlalchemy import and_, or_
from sqlalchemy.orm import session

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

@app.route('/recherche')
def recherche():
    return render_template("pages/recherche.html")

@app.route('/resultats')
def resultats():
    """ Route permettant la recherche plein-texte
    """
    motclef = request.args.get("keyword", None)
    # Liste vide de résultat (qui restera vide par défaut si on n'a pas de mot clé)
    #resultats = []

    # On fait de même pour le titre de la page
    titre = "Résultats"
    if motclef:
        resultats = Individu.query.outerjoin(Diplome).outerjoin(Distinction).outerjoin(Pays_nationalite).outerjoin(Occupation).outerjoin(Domaine_activite).outerjoin(These_enc).filter(
            or_(
                Individu.nom.like("%{}%".format(motclef)),
                Individu.prenom.like("%{}%".format(motclef)),
                Individu.annee_mort.like("%{}%".format(motclef)),
                Individu.annee_naissance.like("%{}%".format(motclef)),
                Individu.date_mort.like("%{}%".format(motclef)),
                Individu.date_naissance.like("%{}%".format(motclef)),
                Diplome.diplome_label.like("%{}%".format(motclef)),
                Distinction.distinction_label.like("%{}%".format(motclef)),
                Pays_nationalite.pays_label.like("%{}%".format(motclef)),
                Occupation.occupation_label.like("%{}%".format(motclef)),
                Domaine_activite.domaine_label.like("%{}%".format(motclef)),
                These_enc.these_label.like("%{}%".format(motclef)),
            )
        ).order_by(Individu.nom.asc()).all()
        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/resultats.html", resultats=resultats, titre=titre)

@app.route('/noticechercheur/<int:individu_id>')
def noticechercheur(individu_id):
    """"Route permettant l'affichage de la notice d'un chercheur
    :param individu_id : Identifiant numérique du chercheur
    """
    individuu = Individu.query.get(individu_id)
    return render_template("pages/noticechercheur.html", individuu=individuu)
#idealement nomchercheur est remplacé par le nomprenom du chercheur
#cette page correspond à la notice complète sur le chercheur
#<string:nomchercheur>
