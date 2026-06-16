from extensions import db


class Etablissement(db.Model):

    __tablename__ = "etablissements"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    adresse = db.Column(
        db.String(200),
        default=""
    )

    def __repr__(self):
        return self.nom
