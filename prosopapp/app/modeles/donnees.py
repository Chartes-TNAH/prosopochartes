from .. app import prosopochartes

class Individu(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    prenom = db.Column(db.Text)
    nom = db.Column(db.Text)
    pays_nationalite_id = db.Column(db.Integer, db.ForeignKey('Pays_nationalite.id'))
    date_naissance = db.Column(db.Text)
    date_mort = db.Column(db.Text)
    image_lien = db.Column(db.Text)
    id_wikidata = db.Column(db.Text)
    id_autorite = db.Column(db.Text)
    diplome_id = db.Column(db.Integer, db.ForeignKey('Diplome.id'))
    these_enc_id = db.Column(db.Integer, db.ForeignKey('These_enc.id'))
    occupation_id = db.Column(db.Integer, db.ForeignKey('Occupation.id'))
    domaine_activite_id = db.Column(db.Integer, db.ForeignKey('Domaine_activite.id'))
    distinction_id = db.Column(db.Integer, db.ForeignKey('Distinction.id'))
    individu_annee_naissance = db.Column(db.Integer)
    individu_annee_mort = db.Column(db.Integer)


class Pays_nationalite
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    pays_label = db.Column(db.Text)

class Occupation
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    occupation_label = db.Column(db.Text)

class Domaine_activite
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    domaine_label = db.Column(db.Text)

class Distinction
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    distinction_label = db.Column(db.Text)

class Diplome
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    diplome_label = db.Column(db.Text)

class These_enc
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    these_label = db.Column(db.Text)
    these_lien = db.Column(db.Text)
    date_soutenance = db.Column(db.Text)


