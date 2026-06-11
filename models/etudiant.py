from app import db


class Etudiant(db.Model):

    __tablename__ = "etudiants"

    id = db.Column(db.Integer, primary_key=True)

    matricule = db.Column(
        db.String(30),
        unique=True,
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

    def __repr__(self):
        return self.nom