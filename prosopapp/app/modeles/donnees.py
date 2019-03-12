#  Importation de la base de données sqlite

from ..app import db

# Création du modèle selon celui de la base de données prosopochartes.sqlite
class Avoir_occupation(db.Model):
    __tablename__ = "avoir_occupation"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    individus = db.relationship("Individu", backref=db.backref("individuals"), single_parent=True)
    occupations = db.relationship("Occupation", backref=db.backref("individuals"), single_parent=True)


    #Avoir_occupation = db.Table("avoir_occupation",
        #db.Column("individu_id", db.Integer, db.ForeignKey("individu.id"), primary_key=True),
        #db.Column("occupation_id", db.Integer, db.ForeignKey("occupation.id"), primary_key=True)
       # )
# Table d'association nécessaire à la déclaration d'une relation many-to-many entre la table indiv8idu et la table Occupation dans notre db


# Table correspondant à un.e chercheu.r.se
# Par souci de simplicité, chaque membre de la table est dans la plupart des cas dans une relation many to one avec les autres tables
# (dans notre base, un.e chercheu.r.se n'a qu'un diplôme, une thèse...)
#Sauf pour le cas de l'occupation, où nous avons créés une relation many to many et qui suppose l'ajout d'une table
#supplémentaire que nous avons dénommées avoir_occupation dans notre modèle sqlite.
# Les relations (or occupation) sont identifiées par des clefs étrangères.
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
    diplome_id = db.Column(db.Integer, db.ForeignKey("diplome.id"))
    these_enc_id = db.Column(db.Integer, db.ForeignKey("these_enc.id"))
    domaine_activite_id = db.Column(db.Integer, db.ForeignKey("domaine_activite.id"))
    distinction_id = db.Column(db.Integer, db.ForeignKey("distinction.id"))
    annee_naissance = db.Column(db.Integer)
    annee_mort = db.Column(db.Integer)
    pays_nationalite = db.relationship("Pays_nationalite", back_populates="individu")
    diplome = db.relationship("Diplome", back_populates="individu")
    these_enc = db.relationship("These_enc", back_populates="individu")
    # La table d'association (nécessaire pour une relation many-to-many)
    # est indiquée grâce au deuxième argument de 'relationship' : 'secondary = avoir_occupation
    # l'utilisation d'un backref à la place du back_populates permet de directement déclarer au sein de la table occupation la relation : (cela nous "économise" l'écriture d'une relation.
    #occupations = db.relationship(
      #"Occupation",
        #secondary=Avoir_occupation,
        #backref="individuals")
    domaine_activite = db.relationship("Domaine_activite", back_populates="individu")
    distinction = db.relationship("Distinction", back_populates="individu")


# Table contenant les pays correspondant à la nationalité des individus
class Pays_nationalite(db.Model):
    __tablename__ = "pays_nationalite"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    pays_label = db.Column(db.Text)
    individu = db.relationship("Individu", back_populates="pays_nationalite")

# Table contenant les métiers exercés par les individus (ex : archiviste, historien)
class Occupation(db.Model):
    __tablename__ = "occupation"
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    occupation_label = db.Column(db.Text)

# Table contenant les champs disciplinaires (ex : moyen-âge, histoire du livre)
class Domaine_activite(db.Model):
    __tablename__ = "domaine_activite"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    domaine_label = db.Column(db.Text)
    individu = db.relationship("Individu", back_populates="domaine_activite")

# Table correspondant à la liste des distinctions reçues par les individus (ex : chevalier de la légion d'honneur)
class Distinction(db.Model):
    __tablename__ = "distinction"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    distinction_label = db.Column(db.Text)
    individu = db.relationship("Individu", back_populates="distinction")

# Table contenant les diplomes des individus (ex : archiviste paléographe, doctorat)
class Diplome(db.Model):
    __tablename__ = "diplome"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    diplome_label = db.Column(db.Text)
    individu = db.relationship("Individu", back_populates="diplome")

# Table contenant les informations sur les thèses d'école (titre, date de soutenance, lien vers la thèse)
class These_enc(db.Model):
    __tablename__ = "these_enc"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    these_label = db.Column(db.Text)
    these_lien = db.Column(db.Text)
    date_soutenance = db.Column(db.Integer)
    individu = db.relationship("Individu", back_populates="these_enc")


