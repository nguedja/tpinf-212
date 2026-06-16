from extensions import db


class Etudiant(db.Model):

    __tablename__ = "etudiants"

    id = db.Column(db.Integer, primary_key=True)

    etablissement_id = db.Column(
        db.Integer,
        db.ForeignKey("etablissements.id"),
        nullable=False
    )

    matricule = db.Column(
        db.String(30),
        nullable=False
    )

    nom = db.Column(
        db.String(100),
        nullable=False
    )

    filiere = db.Column(
        db.String(50),
        nullable=False
    )

    etablissement = db.relationship(
        "Etablissement",
        backref=db.backref("etudiants", lazy=True)
    )

    def __repr__(self):
        return self.nom