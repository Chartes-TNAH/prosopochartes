from flask import render_template, url_for, request

#cette commande nous permet de relier nos templates à nos urls - routes
#On importe url_for pour construire des URL vers les fonctions et les pages html
from .modeles.donnees import Individu, Pays_nationalite, Occupation, Diplome, Distinction, Domaine_activite, These_enc, Avoir_occupation

#cette commande nous permet de relier les classes de notre modèle de données pour pouvoir ensuite les requêter.
from sqlalchemy import and_, or_
from sqlalchemy.orm import session

from app.app import app
#Cette commande permet d'importer de notre package app, la variable app, qui instancie notre application.
from .constantes import CHERCHEURS_PAR_PAGE
#Cette commande permet d'importer le nombre de chercheurs par pages depuis notre dossier constantes.py

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
#Nous stockons dans la variable individu une liste contenant les valeurs de notre table individu, c'est ce qui nous permet
#de faire le lien vers son template qui se trouve dans le dossier "pages" (avec l'utilisation surtout de la fonction render_template)
    return render_template("pages/chercheurs.html", individus=individus)

@app.route('/recherche')
def recherche():
    occupations = Occupation.query.all()
    pays = Pays_nationalite.query.all()
    activites = Domaine_activite.query.all()
    distinctions = Distinction.query.all()
    diplomes = Diplome.query.all()
    return render_template("pages/recherche.html", occupations=occupations, pays=pays, activites=activites, distinctions=distinctions, diplomes=diplomes)

@app.route('/resultats')
def resultats():
    """ Route permettant la recherche plein-texte
    """
    motclef = request.args.get("keyword", None)
    #On stocke dans la variable mot clef une liste qui est destinée à contenir la valeur du mot clé rentré par l'utilisateur dans la barre de recherche
    page = request.args.get("page", 1)
    #On stocke dans la variable page une liste qui est destinée à contenir la valeur du numéro de page

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    #Si le numéro de la page est une chaîne de caractères composée uniquement de chiffres
    #Alors on la recaste en integer
    #Sinon, le numéro de la page est égal à 1

    # On crée une liste vide de résultat (qui restera vide par défaut si on n'a pas de mot clé)
    resultats = []

    # On crée une variable titre qui nous servira à afficher le résultat de notre requête
    titre = "Résultats"

    if motclef:
    #Si on a un mot clé, on requête toutes les tables de notre base de donnée pour vérifier s'il y a des correspondances
    #Le résultat de cette requête est stocké dans la liste resultats = []
        resultats = Individu.query.outerjoin(Diplome).join(Avoir_occupation).outerjoin(Distinction).outerjoin(Pays_nationalite).outerjoin(Domaine_activite).outerjoin(These_enc).filter(
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
                Avoir_occupation.occupations.occupation_label.like("%{}%".format(motclef)),
                Domaine_activite.domaine_label.like("%{}%".format(motclef)),
                These_enc.these_label.like("%{}%".format(motclef)),
            )
        ).order_by(Individu.nom.asc()).paginate(page=page, per_page=CHERCHEURS_PAR_PAGE)
        titre = "Voici les résultats de votre recherche pour : '"+ motclef + "'."
        #On affiche une phrase qui indiquera les résultats de la recherche en fonction du mot clé rentré par l'utilisateur
        #Cette variable titre sera réutilisée dans la page resultats.html
    return render_template("pages/resultats.html", resultats=resultats, titre=titre, keyword=motclef)
    #On retourne la page resultats.html, et on indique à quoi correspondent les variables resultats, titre et keyword,
    #qui seront appelées ensuite au sein des pages html


@app.route('/resultats_avances')
def resultats_avances():
    """ Route permettant d'effectuer une recherche dite avancée sur la base
    de données, en requêtant les champs suivantes : occupation, distinction,
    pays de nationalité, domaine d'activité, titre de thèse d'école,
    ainsi que date de soutenance, de décès et de mort (il est possible de requêter
    les dates précises, ou de définir un intervalle)
    """


    motclef = request.args.get("motclef", None)
    naissanceMin = request.args.get("naissanceMin", None)
    naissanceExacte = request.args.get("naissanceExacte", None)
    naissanceMax = request.args.get("naissanceMax", None)
    mortMin = request.args.get("mortMin", None)
    mortExacte = request.args.get("mortExacte", None)
    mortMax = request.args.get("mortMax", None)
    theseMin = request.args.get("theseMin", None)
    theseExacte = request.args.get("theseExacte", None)
    theseMax = request.args.get("theseMax", None)
    theseLabel = request.args.get("theseLabel", None)
    occupations = request.args.get("occupations", None)
    pays = request.args.get("pays", None)
    domaine_activite = request.args.get("domaine_activite", None)
    distinction = request.args.get("distinction", None)
    diplome = request.args.get("diplome", None)


    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    requete = Individu.query.outerjoin(Diplome).outerjoin(Distinction).outerjoin(Pays_nationalite).outerjoin(Occupation).outerjoin(Domaine_activite).outerjoin(These_enc)

    if motclef :
        requete = requete.filter(or_(
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
            ))
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
        requete = requete.filter(These_enc.date_soutenance >= theseMin)
    if theseExacte :
        requete = requete.filter(These_enc.date_soutenance == theseExacte)
    if theseMax :
        requete = requete.filter(These_enc.date_soutenance <= theseMax)
    if theseLabel :
        requete = requete.filter(These_enc.these_label.like("%{}%".format(theseLabel)))
    if occupations and occupations != "all":
        requete = requete.filter(Occupation.occupation_label == occupations)
    if pays and pays != "all":
        requete = requete.filter(Pays_nationalite.pays_label == pays)
    if domaine_activite and domaine_activite != "all":
       requete = requete.filter(Domaine_activite.domaine_label == domaine_activite)
    if distinction and distinction != "all":
        requete = requete.filter(Distinction.distinction_label == distinction)
    if diplome and diplome != "all":
        requete = requete.filter(Diplome.diplome_label == diplome)




    requete = requete.order_by(Individu.nom.asc()).paginate(page=page, per_page=CHERCHEURS_PAR_PAGE)

    return render_template(
        "pages/resultats_avances.html",
        motclef=motclef,
        naissanceMin=naissanceMin,
        naissanceExacte=naissanceExacte,
        naissanceMax=naissanceMax,
        mortMin=mortMin,
        mortExacte=mortExacte,
        mortMax=mortMax,
        theseMin=theseMin,
        theseExacte=theseExacte,
        theseMax=theseMax,
        theseLabel=theseLabel,
        occupations=occupations,
        pays=pays,
        domaine_activite=domaine_activite,
        distinction=distinction,
        diplome=diplome,
        requete=requete
        )



@app.route('/noticechercheur/<int:individu_id>')
def noticechercheur(individu_id):
    """"Route permettant l'affichage de la notice d'un chercheur
    :param individu_id : variable qui nous permettra de lier nos pages via des url_for et qui correspond à l'id de notre chercheur.
    """
    individuu = Individu.query.get(individu_id)
    return render_template("pages/noticechercheur.html", individuu=individuu)

