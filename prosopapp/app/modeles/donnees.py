#  Importation de la base de données sqlite

from ..app import basedonnees

# Création du modèle selon celui de la base de données prosopochartes.sqlite

# Table correspondant à un.e chercheu.r.se
# Par souci de simplicité, chaque membre de la table est dans une relation many to one avec les autres tables
# (dans notre base, un.e chercheu.r.se n'a qu'un diplôme, une distinction...)
# Les relations sont donc identifiées par des clefs étrangères
class Individu(db.Model):
    __tablename__ = "individu"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    prenom = db.Column(db.Text)
    nom = db.Column(db.Text)
    pays_nationalite_id = db.Column(db.Integer, db.ForeignKey('pays_nationalite.id'))
    date_naissance = db.Column(db.Text)
    date_mort = db.Column(db.Text)
    image_lien = db.Column(db.Text)
    id_wikidata = db.Column(db.Text)
    id_autorite = db.Column(db.Text)
    diplome_id = db.Column(db.Integer, db.ForeignKey('diplome.id'))
    these_enc_id = db.Column(db.Integer, db.ForeignKey('these_enc.id'))
    occupation_id = db.Column(db.Integer, db.ForeignKey('occupation.id'))
    domaine_activite_id = db.Column(db.Integer, db.ForeignKey('domaine_activite.id'))
    distinction_id = db.Column(db.Integer, db.ForeignKey('distinction.id'))
    individu_annee_naissance = db.Column(db.Integer)
    individu_annee_mort = db.Column(db.Integer)
    pays_nationalite = db.Relationship("Pays_nationalite", back_populate="individu")
    diplome =  db.Relationship ("Diplome", back_populate="individu")
    these_enc = db.Relationship("These_enc", back_populate="individu")
    occupation = db.Relationship("Occupation", back_populate="individu")
    domaine_activite = db.Relationship("Domaine_activite", back_populate="individu")
    distinction = db.Relationship("Distinction", back_populate="individu")

# Table contenant les pays correspondant à la nationalité des individus
class Pays_nationalite :
    __tablename__ = "pays_nationalite"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    pays_label = db.Column(db.Text)
    individu = db.Relationship("Individu", back_populate="pays_nationalite")

# Table contenant les métiers exercés par les individus (ex : archiviste, historien)
class Occupation :
    __tablename__ = "occupation"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    occupation_label = db.Column(db.Text)
    individu = db.Relationship("Individu", back_populate="occupation")

# Table contenant les champs disciplinaires (ex : moyen-âge, histoire du livre)
class Domaine_activite :
    __tablename__ = "domaine_activite"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    domaine_label = db.Column(db.Text)
    individu = db.Relationship("Individu", back_populate="domaine_activite")

# Table correspondant à la liste des distinctions reçues par les individus (ex : chevalier de la légion d'honneur)
class Distinction :
    __tablename__ = "distinction"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    distinction_label = db.Column(db.Text)
    individu = db.Relationship("Individu", back_populate="distinction")

# Table contenant les diplomes des individus (ex : archiviste paléographe, doctorat)
class Diplome :
    __tablename__ = "diplome"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    diplome_label = db.Column(db.Text)
    individu = db.Relationship("Individu", back_populate="diplome")

# Table contenant les informations sur les thèses d'école (titre, date de soutenance, lien vers la thèse)
class These_enc :
    __tablename__ = "these_enc"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    these_label = db.Column(db.Text)
    these_lien = db.Column(db.Text)
    date_soutenance = db.Column(db.Text)
    individu = db.Relationship("Individu", back_populate="these_enc")


