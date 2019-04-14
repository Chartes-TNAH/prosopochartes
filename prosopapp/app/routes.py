from flask import render_template, url_for, request, send_file, redirect
# L'import de render_template nous permet de relier nos templates à nos urls - routes
# L'import de url_for permet de construire des URL vers les fonctions et les pages html
# L'import de la commande request nous permet d'importer les noms de types d'objets moins courant que int ou str, et de pouvoir ainsi les utiliser
# dans des fonctions tels que insinstance.()
# L'import de send_file nous permet d'envoyer des fichiers au client
# L'import de redirect nous permet de créer des fonctions qui retournent une redirection vers l'url d'une autre route

from .modeles.donnees import Individu, Pays_nationalite, Occupation, Diplome, Distinction, Domaine_activite, These_enc, Avoir_occupation
# Cette commande nous permet d'importer les classes de notre modèle de données dans notre application, pour pouvoir ensuite les requêter.

from sqlalchemy import and_, or_
# Cette commande nous permet d'utiliser les opérateurs 'and' et 'or' dans nos fonctions de requêtage de notre base de données

from .app import app
# Cette commande permet d'importer, depuis notre package app, la variable app qui instancie notre application.

from .constantes import CHERCHEURS_PAR_PAGE
# Cette commande permet d'importer le nombre de chercheurs par pages depuis notre dossier constantes.py

import random
# Cette commande nous permet de générer des nombres aléatoires

# Les commandes suivantes nous permettent de créer différentes routes - qui correspondent à l'URL des différents pages
# de notre application :

@app.route('/')
def accueil ():
    return render_template("pages/accueil.html", title="accueil")
    # La fonction render_template prend comme premier argument le chemin du template et en deuxième des arguments nommés, qui
    # peuvent ensuite être réutilisés en tant que variables dans les templates.

@app.route('/chercheurs')
def chercheurs():
    """Route permettant d'afficher certains champs pour les notices de tous les chercheurs"""
    individus = Individu.query.order_by(Individu.nom.asc()).all()
    # Nous stockons dans la variable individu une liste contenant les valeurs de notre table individu, ce qui nous permet
    # de faire le lien vers son template qui se trouve dans le dossier "pages" (avec notamment l'utilisation de la fonction render_template)
    return render_template("pages/chercheurs.html", individus=individus)

@app.route('/recherche')
def recherche():
    """Route permettant de créer le formulaire de recherche avancée"""
    occupations = Occupation.query.order_by(Occupation.occupation_label).all()
    pays = Pays_nationalite.query.order_by(Pays_nationalite.pays_label).all()
    activites = Domaine_activite.query.order_by(Domaine_activite.domaine_label).all()
    distinctions = Distinction.query.order_by(Distinction.distinction_label).all()
    diplomes = Diplome.query.order_by(Diplome.diplome_label).all()
    # Les variables ci-dessus permettent de stocker les valeurs des tables concernées,
    # ce qui nous permet par la suite de les faire apparaître dans des menus déroulants dans notre page recherche.html
    return render_template("pages/recherche.html", occupations=occupations, pays=pays, activites=activites, distinctions=distinctions, diplomes=diplomes)

@app.route('/resultats')
def resultats():
    """ Route permettant la recherche plein-texte
    """
    motclef = request.args.get("motclef", None)
    # On stocke dans la variable mot-clef une liste qui est destinée à contenir la valeur du mot-clé rentré par l'utilisateur dans la barre de recherche
    page = request.args.get("page", 1)
    # On stocke dans la variable page une liste qui est destinée à contenir la valeur du numéro de page

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    # Si le numéro de la page est une chaîne de caractères composée uniquement de chiffres
    # Alors on la recaste en integer
    # Sinon, le numéro de la page est égal à 1

    resultats = []
    # On crée une liste vide de résultats (qui restera vide par défaut si on n'a pas de mot clé)
    titre = "Aucun mot clef entré"

    if motclef:
    # Si on a un mot-clé, on requête toutes les tables de notre base de données pour vérifier s'il y a des correspondances
    # Le résultat de cette requête est stocké dans la liste resultats = []
        resultats = Individu.query.filter(
            or_(
                Individu.nom.like("%{}%".format(motclef)),
                Individu.prenom.like("%{}%".format(motclef)),
                Individu.annee_mort.like("%{}%".format(motclef)),
                Individu.annee_naissance.like("%{}%".format(motclef)),
                Individu.date_mort.like("%{}%".format(motclef)),
                Individu.date_naissance.like("%{}%".format(motclef)),
                Individu.diplome.has((Diplome.diplome_label).like("%{}%".format(motclef))),
                # has signifie : le critère est-il true ?
                Individu.distinction.has((Distinction.distinction_label).like("%{}%".format(motclef))),
                Individu.pays_nationalite.has((Pays_nationalite.pays_label).like("%{}%".format(motclef))),
                Individu.domaine_activite.has((Domaine_activite.domaine_label).like("%{}%".format(motclef))),
                Individu.these_enc.has((These_enc.these_label).like("%{}%".format(motclef))),
                Individu.occupations.any((Occupation.occupation_label).like("%{}%".format(motclef))),
                # any signifie : au moins un des critères est true, nous l'utilisons ici puisque nous cherchons à requêter un champ pouvant contenir plusieurs valeurs.
            )
        ).order_by(Individu.nom.asc()).paginate(page=page, per_page=CHERCHEURS_PAR_PAGE)
        titre = "Voici les résultats de votre recherche pour : '"+ motclef + "'."
        # On affiche une phrase de titre qui indiquera les résultats de la recherche en fonction du mot-clé rentré par l'utilisateur
        # Cette variable titre sera réutilisée dans la page resultats.html
    return render_template("pages/resultats.html", resultats=resultats, titre=titre, motclef=motclef)
    # On retourne la page resultats.html, et on indique à quoi correspondent les variables resultats, titre et keyword,
    # qui seront appelées ensuite au sein des pages html


@app.route('/resultats_avances')
def resultats_avances():
    """ Route permettant d'effectuer une recherche dite avancée sur la base
    de données, en requêtant les champs suivants : occupation, distinction,
    pays de nationalité, domaine d'activité, titre de thèse d'école,
    ainsi que date de soutenance, de décès et de mort (il est possible de requêter
    les dates précises, ou de définir un intervalle)
    """

    # Il faut premièrement aller récupérer les valeurs entrées dans le formulaire de recherche par l'utilisateur :
    # Ces valeurs sont stockées dans des variables, auxquelles se réfère l'attribut name des éléments select ou input
    # de la page de formulaire recherche.html
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
    asc = request.args.get("asc", None)
    desc = request.args.get("desc", None)

    # Mêmes commentaires que pour la pagination effectuée pour la fonction résultats
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    message = []
    # Cette variable sert à stocker les potentiels messages d'erreurs :

    dates = [naissanceMin, naissanceExacte, naissanceMax, mortMin, mortExacte, mortMax, theseMin, theseExacte, theseMax]
    # Cette liste nous sert à regrouper tous les champs relatifs à une  et à les stocker dans une variable
    # Nous nous en servons lorsque nous effectuons un traitement identique sur tous les champs de date de notre formulaire :
    # par exemple, une boucle qui permet d'afficher un message d'erreur commun

    requete = Individu.query
    # Déclaration d'une variable requete qui nous servira à stocker les recherches réalisées et à combiner plusieurs champs lors du requêtage.
    # ainsi qu'à alléger la syntaxe de notre code
    # Notre requete étant ensuite filtrée, nous lui attribuons la valeur initiale permettant ensuite de filter les champs de la table individu.

    # Le premier champ de la recherche avancée est en fait le même champ que celui de la recherche simple, c'est-à-dire de la fonction resultats()
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

    # Pour la suite des champs, nous avons utilisé d'autres 'if' et non pas 'elif' : en effet, en utilisant 'elif', chaque condition
    # n'aurait été prise en compte que si la condition précédente n'avait pas été remplie.
    # Or, nous voulons au contraire une fonction qui prenne en compte tous les paramètres entrés dans chaque champ du formulaire de recherche avancée,
    # en ajoutant à chaque fois un nouveau filtre à la valeur précédente de la variable requete

    if naissanceMin :
        requete = requete.filter(Individu.annee_naissance >= naissanceMin)
    # Si une date de naissance minimale a été renseignée, on filtre la variable requête pour ne garder que les chercheurs nés après cette date
    if naissanceExacte :
        requete = requete.filter(Individu.annee_naissance == naissanceExacte)
    # Si une date de naissance précise a été renseignée, on filtre la variable requête pour ne garder que les chercheurs nés à cette date
    if naissanceMax :
        requete = requete.filter(Individu.annee_naissance <= naissanceMax)
    # Si une date de naissance maximale a été renseignée, on filtre la variable requête pour ne garder que les chercheurs nés avant cette date
    # Les conditions ci-dessous suivent le même modèle, mais avec les dates de mort et de soutenance de thèse d'école :
    if mortMin :
        requete = requete.filter(Individu.annee_mort >= mortMin)
    if mortExacte :
        requete = requete.filter(Individu.annee_mort == mortExacte)
    if mortMax :
        requete = requete.filter(Individu.annee_mort <= mortMax)
    if theseMin :
        requete = requete.filter(Individu.these_enc.has(These_enc.date_soutenance >= theseMin))
    if theseExacte :
        requete = requete.filter(Individu.these_enc.has(These_enc.date_soutenance == theseExacte))
    if theseMax :
        requete = requete.filter(Individu.these_enc.has(These_enc.date_soutenance <= theseMax))
    if theseLabel :
        requete = requete.filter(Individu.these_enc.has((These_enc.these_label).like("%{}%".format(theseLabel))))
    # Si une chaîne de caractère a été renseignée, filtre la variable requête pour ne garder que les titres de thèses où cette chaîne de caractères est présente
    if occupations and occupations != "all":
        requete = requete.filter(Individu.occupations.any(Occupation.occupation_label == occupations))
    # Si une valeur de la table occupations a été sélectionnée dans le menu déroulant associé, on filtre la variable requete pour ne garder que les chercheurs ayant cette occupation
    # Les conditions ci-dessous suivent le même principe :
    if pays and pays != "all":
        requete = requete.filter(Individu.pays_nationalite.has(Pays_nationalite.pays_label == pays))
    if domaine_activite and domaine_activite != "all":
       requete = requete.filter(Individu.domaine_activite.has(Domaine_activite.domaine_label == domaine_activite))
    if distinction and distinction != "all":
        requete = requete.filter(Individu.distinction.has(Distinction.distinction_label == distinction))
    if diplome and diplome != "all":
        requete = requete.filter(Individu.diplome.has(Diplome.diplome_label == diplome))

    # Les conditions ci-dessous permettent à l'utilisateur de choisir s'il souhaite obtenir les résultats dans un ordre
    # alphabétique croissant ou décroissant
    # Il n'a pas été possible de n'utiliser qu'une seule variable (par exemple : if desc / if not desc), car, si le bouton lié à "desc"
    # était appuyé à un moment, le paramètre "if desc" continuait d'être pris en compte, et ce même si le bouton était décoché. Il a donc
    # fallu faire appel à deux variables, pour que l'activation d'un bouton "écrase" la valeur de la variable liée à l'autre bouton.
    if asc :
        requete = requete.order_by(Individu.nom.asc())
    if desc :
        requete = requete.order_by(Individu.nom.desc())
    # Pour éviter que les résultats ne s'affichent autrement que dans un ordre alphabétique si aucun bouton n'est sélectionné, cette
    # condition permet de garder l'ordre croissant si rien n'est sélectionné sur le formulaire (cette notion d' "ordre
    # croissant par défaut" est représentée sur le formulaire par l'illusion que le bouton "A-Z" est pré-coché)
    if not asc and not desc :
        requete = requete.order_by(Individu.nom.asc())

    # Ci-dessous se trouvent certains messages d'erreur correspondant à des erreurs spécifiques :
    # Nous les faisons apparaître en utilisant également un "if", et non un "else", car, compte-tenu de la structure de notre fonction,
    # si nous choisissons le "else", il ne va entrer en jeu que si aucune des conditions "if" n'est remplie, c'est-à-dire, dans notre
    # cas, si aucun champs du formulaire n'a été renseigné (n'attribuant ainsi aucune valeur aux variables).

    if naissanceMin and naissanceMax and naissanceMin >= naissanceMax:
        message = "Vous avez renseigné une date de naissance minimale postérieure à la date de naissance maximale."
    if mortMin and mortMax and mortMin >= mortMax:
        message = "Vous avez renseigné une date de mort minimale postérieure à la date de mort maximale."
    if theseMin and theseMax and theseMin >= theseMax:
        message = "Vous avez renseigné une date de soutenance minimale postérieure à la date de soutenance maximale."
    # Ces trois messages interviennent si, dans le cas d'un intervalle, les champs minimum et maximum sont tous deux renseignés,
    # mais que la valeur minimale est supérieure à la maximale.

    for date in dates :
        if date and date.isdigit() is False :
            message = "L'un des champs date contient des caractères qui ne sont pas des chiffres"
    # Il s'agit de boucler sur les champs se référant à une date, et d'afficher un message si l'un de ces champs a été renseigné autremen
    # qu'avec des valeurs numériques. Nous avons choisi d'utiliser .isdigit() car, les valeurs entrées dans les champs du formulaires
    # correspondant à des str, cette solution était plus simple que de d'abord passer par un typage en int des valeurs renseignées dans ce champ

    requete = requete.paginate(page=page, per_page=CHERCHEURS_PAR_PAGE)
    #requete = requete.order_by(Individu.nom.asc()).paginate(page=page, per_page=CHERCHEURS_PAR_PAGE)

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
        requete=requete,
        asc=asc,
        desc=desc
        )



@app.route('/noticechercheur/<int:individu_id>')
def noticechercheur(individu_id):
    """"Route permettant l'affichage de la notice d'un chercheur
    :param individu_id : variable qui nous permettra de lier nos pages via des url_for et qui correspond à l'id de notre chercheur.
    """
    individuu = Individu.query.get(individu_id)
    return render_template("pages/noticechercheur.html", individuu=individuu)

@app.route('/aleatoire')
def aleatoire():
    """Route génère un nombre aléatoire, et retourne une redirection vers l'url composée de noticechercheur et de ce nombre aléatoire,
    ce qui déclenche de là la fonction noticechercheur prenant ce nombre aléatoire en paramètre : cela affiche donc une notice aléatoirement"""

    nbMax = Individu.query.count()
    # Nous comptons le nombre d'entrées dans la table individu, et assignons ce nombre à la variable nbMax

    nb = random.randint(1, nbMax)
    # Nous générons grâce à la fonction random un integer aléatoire pouvant aller de 1 à la valeur de nbMax
    # Cela nous permet de générer un nombre qui correspond à un id de la table individu, tout en permettant à la fonction de continuer
    # de marcher si nous rajoutons des individus dans la base

    # Notons que cette technique marche parfaitement car nous n'avons jamais supprimé une entrée de la base : le nombre d'individus
    # correspond aux valeurs des id ; il faudrait s'y prendre autrement si certains id avaient une valeur supérieure au nombre maximal
    # d'individus dans la base (un message d'erreur est néanmoins prévu sur la page noticechercheur.html)

    return redirect(url_for('noticechercheur', individu_id=nb))
    # Comme url_for('noticechercheur') demande la prise en compte du paramètre individu_id, il nous faut 'recomposer' l'url sous forme
    # de chaine de caractères pour parvenir à nos fins

@app.route('/telechargement')
def telechargement():
    """Route permettant d'afficher la page telechargement.html"""
    return render_template("pages/telechargement.html")

@app.route('/download')
def download():
    """Route permettant à l'utilisateur de télécharger le fichier prosopochartes.sqlite (base de données sur laquelle se base l'application)"""
    f = '../prosopochartes.sqlite'
    return send_file(f, attachment_filename='prosopochartes.sqlite', as_attachment=True)