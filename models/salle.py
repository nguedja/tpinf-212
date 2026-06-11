from extensions import db


class Salle(db.Model):

    __tablename__ = "salles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    capacite = db.Column(
        db.Integer,
        nullable=False
    )

    type_salle = db.Column(
        db.String(20),
        nullable=False
    )

    def __repr__(self):
        return self.nom