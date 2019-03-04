from flask import render_template
from app import app

@app.route('/')
@app.route('/accueil')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('accueil.html', title='Home', user=user, posts=posts)

@app.route('/chercheurs')
@app.route('/recherche')
@app.route('/resultats')
#cette route correspond à la page qui affichera les notices abrégées des résultats
# à voir si on choisit de la conserver sous la dénomination résultat où si l'on préfère un nom qui reprend les mots-clés?
@app.route('/<str:nomchercheur>')
# idealement nomchercheur est remplacé par le nomprenom du chercheur
#cette page correspond à la notice complète sur le chercheur
