from flask import render_template, url_for, request
#Cette commande nous permet de relier nos templates à nos urls - routes
#On importe url_for pour construire des URL vers les fonctions et les pages html
#Cette commande nous permet d'importer les noms de types d'objets moins courant que int ou str, et de pouvoir ainsi les utiliser
#dans des fonctions tels que insinstance.()

from .modeles.donnees import Individu, Pays_nationalite, Occupation, Diplome, Distinction, Domaine_activite, These_enc, Avoir_occupation
#Cette commande nous permet de relier les classes de notre modèle de données pour pouvoir ensuite les requêter.

from sqlalchemy import and_, or_
#Cette commande nous permet d'utiliser les opérateurs 'and' et 'or' dans nos fonctions de requêtage de notre base de données

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
    """Route permettant de créer le formulaire de recherche avancée"""
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
    motclef = request.args.get("motclef", None)
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

    if motclef:
    #Si on a un mot clé, on requête toutes les tables de notre base de donnée pour vérifier s'il y a des correspondances
    #Le résultat de cette requête est stocké dans la liste resultats = []
        resultats = Individu.query.filter(
            or_(
                Individu.nom.like("%{}%".format(motclef)),
                Individu.prenom.like("%{}%".format(motclef)),
                Individu.annee_mort.like("%{}%".format(motclef)),
                Individu.annee_naissance.like("%{}%".format(motclef)),
                Individu.date_mort.like("%{}%".format(motclef)),
                Individu.date_naissance.like("%{}%".format(motclef)),
                #has signifie : est-ce que le critère est true
                Individu.diplome.has((Diplome.diplome_label).like("%{}%".format(motclef))),
                Individu.distinction.has((Distinction.distinction_label).like("%{}%".format(motclef))),
                Individu.pays_nationalite.has((Pays_nationalite.pays_label).like("%{}%".format(motclef))),
                Individu.domaine_activite.has((Domaine_activite.domaine_label).like("%{}%".format(motclef))),
                Individu.these_enc.has((These_enc.these_label).like("%{}%".format(motclef))),
                # any signifie : au moins un des critères est true, nous l'utilisons ici puisque nous cherchons à requêter un champ pouvant contenir plusieurs valeurs.
                Individu.occupations.any((Occupation.occupation_label).like("%{}%".format(motclef))),
            )
        ).order_by(Individu.nom.asc()).paginate(page=page, per_page=CHERCHEURS_PAR_PAGE)
        titre = "Voici les résultats de votre recherche pour : '"+ motclef + "'."
        #On affiche une phrase de titre qui indiquera les résultats de la recherche en fonction du mot clé rentré par l'utilisateur
        #Cette variable titre sera réutilisée dans la page resultats.html
    return render_template("pages/resultats.html", resultats=resultats, titre=titre, motclef=motclef)
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

# Il faut premièrement aller récupérer les valeurs entrées dans le formulaire de rechercher par le biais de leurs attributs name.
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

#Même commentaires que pour la pagination effectuées pour la fonction résultats
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

# Cette variable sert à faire apparaître les messages d'erreurs :
    message = []

# Cette liste nous sert à regrouper tous les champs relatifs à une date, pour pouvoir créer des boucles et alléger le code
# dans les cas où nous effectuons un traitement identitques sur ces types de champs (pour caster le contenu assigné
# à ces variables par exemple, ou pour faire apparaître certains messages d'erreurs)
    dates = [naissanceMin, naissanceExacte, naissanceMax, mortMin, mortExacte, mortMax, theseMin, theseExacte, theseMax]

#Déclaration d'une variable requete qui nous servira à stocker les recherches réalisées et à combiner plusieurs champs lors du requêtage.
# Notre requete étant ensuite filtrée, nous lui attribuons la valeur initiale permettant ensuite de filter les champs de la table individu.
    requete = Individu.query
    # Le premier champ de la recherche avancée est en fait le même champ que celui de la recherche générale
    if motclef :
        requete = requete.filter(or_(
            Individu.nom.like("%{}%".format(motclef)),
            Individu.prenom.like("%{}%".format(motclef)),
            Individu.annee_mort.like("%{}%".format(motclef)),
            Individu.annee_naissance.like("%{}%".format(motclef)),
            Individu.date_mort.like("%{}%".format(motclef)),
            Individu.date_naissance.like("%{}%".format(motclef)),
            # has signifie : est-ce que le critère est true
            Individu.diplome.has((Diplome.diplome_label).like("%{}%".format(motclef))),
            Individu.distinction.has((Distinction.distinction_label).like("%{}%".format(motclef))),
            Individu.pays_nationalite.has((Pays_nationalite.pays_label).like("%{}%".format(motclef))),
            Individu.domaine_activite.has((Domaine_activite.domaine_label).like("%{}%".format(motclef))),
            Individu.these_enc.has((These_enc.these_label).like("%{}%".format(motclef))),
            # any signifie : au moins un des critères est true, nous l'utilisons ici puisque nous cherchons à requêter un champ pouvant contenir plusieurs valeurs.
            Individu.occupations.any((Occupation.occupation_label).like("%{}%".format(motclef))),
            ))
    # Pour la suite des champs, nous avons utilisé d'autres 'if' et non pas 'elif' : en effet, en utilisant 'elif', les conditions ci-desous
    # n'auraient été prises en compte que si la condition précédente n'avait pas été remplie.
    # Or, nous ne souhaitons une fonction qui agisse ansi : "si pas de données dans ce champ, voir s'il y en a dans le suivant",
    # mais au contraire une fonction qui prenne en compte tous les paramètres entrés dans chaque champ du formulaire de recherche avancée
    # en ajoutant à chaque fois un nouveau filtre à l'état précédent de la variable requete
    if naissanceMin and isinstance(naissanceMin, str) and naissanceMin.isdigit() :
        naissanceMin = int(naissanceMin)
        requete = requete.filter(Individu.annee_naissance >= naissanceMin)
    # Dans la condition ci-dessus et dans les conditions suivantes qui font référence à une date (type int dans notre base sqlite),
    # nous avons choisi de retyper le texte entré dans le champ du formulaire par l'utilisateur (dans le cas où ce texte est composé de cractères numériques) en integer.
    # En effet, même si les opérateurs >=, == et <= fonctionnent sur des caractères numériques même s'ils sont de type str,
    # les retyper en integer nous permet par la suite de générer un message d'erreur lorsqu'un caractère qui n'est pas un chiffre est tapé dans ces champs
    if naissanceExacte and isinstance(naissanceExacte, str) and naissanceExacte.isdigit() :
        naissanceExacte = int(naissanceExacte)
        requete = requete.filter(Individu.annee_naissance == naissanceExacte)
    if naissanceMax and isinstance(naissanceMax, str) and naissanceMax.isdigit() :
        naissanceMax = int(naissanceMax)
        requete = requete.filter(Individu.annee_naissance <= naissanceMax)
    if mortMin and isinstance(mortMin, str) and mortMin.isdigit() :
        mortMin = int(mortMin)
        requete = requete.filter(Individu.annee_mort >= mortMin)
    if mortExacte and isinstance(mortExacte, str) and mortExacte.isdigit() :
        mortExacte = int(mortExacte)
        requete = requete.filter(Individu.annee_mort == mortExacte)
    if mortMax and isinstance(mortMax, str) and mortMax.isdigit() :
        mortMax = int(mortMax)
        requete = requete.filter(Individu.annee_mort <= mortMax)
    if theseMin and isinstance(theseMin, str) and theseMin.isdigit() :
        theseMin = int(theseMin)
        requete = requete.filter(Individu.these_enc.has(These_enc.date_soutenance >= theseMin))
    if theseExacte and isinstance(theseExacte, str) and theseExacte.isdigit() :
        theseExacte = int(theseExacte)
        requete = requete.filter(Individu.these_enc.has(These_enc.date_soutenance == theseExacte))
    if theseMax and isinstance(theseMax, str) and theseMax.isdigit() :
        theseMax = int(theseMax)
        requete = requete.filter(Individu.these_enc.has(These_enc.date_soutenance <= theseMax))
    if theseLabel :
        requete = requete.filter(Individu.these_enc.has((These_enc.these_label).like("%{}%".format(theseLabel))))
    if occupations and occupations != "all":
        requete = requete.filter(Individu.occupations.any(Occupation.occupation_label == occupations))
    if pays and pays != "all":
        requete = requete.filter(Individu.pays_nationalite.has(Pays_nationalite.pays_label == pays))
    if domaine_activite and domaine_activite != "all":
       requete = requete.filter(Individu.domaine_activite.has(Domaine_activite.domaine_label == domaine_activite))
    if distinction and distinction != "all":
        requete = requete.filter(Individu.distinction.has(Distinction.distinction_label == distinction))
    if diplome and diplome != "all":
        requete = requete.filter(Individu.diplome.has(Diplome.diplome_label == diplome))

    # Ci-dessous se trouvent certains messages d'erreur correspondant à des erreurs spécifiques
    if naissanceMin and naissanceMax and naissanceMin >= naissanceMax:
        message = "Vous avez renseigné une date de naissance minimale postérieure à la date de naissance maximale."
    if mortMin and mortMax and mortMin >= mortMax:
        message = "Vous avez renseigné une date de mort minimale postérieure à la date de mort maximale."
    if theseMin and theseMax and theseMin >= theseMax:
        message = "Vous avez renseigné une date de soutenance minimale postérieure à la date de soutenance maximale."

    # Ci-dessous une boucle qui d'afficher un message d'erreur si un champ date n'est pas vide, mais n'est pas rempli
    # avec des integers
    for date in dates :
        if date and isinstance(date, int) is False :
            message = "L'un des champs date contient des caractères qui ne sont pas des chiffres"


    requete = requete.order_by(Individu.nom.asc()).paginate(page=page, per_page=CHERCHEURS_PAR_PAGE)

    titre = "Résultats"
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
        titre=titre,
        message=message,
        requete=requete
        )



@app.route('/noticechercheur/<int:individu_id>')
def noticechercheur(individu_id):
    """"Route permettant l'affichage de la notice d'un chercheur
    :param individu_id : variable qui nous permettra de lier nos pages via des url_for et qui correspond à l'id de notre chercheur.
    """
    individuu = Individu.query.get(individu_id)
    return render_template("pages/noticechercheur.html", individuu=individuu)

