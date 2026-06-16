from extensions import db


class Creneau(db.Model):

    __tablename__ = "creneaux"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    etablissement_id = db.Column(
        db.Integer,
        db.ForeignKey("etablissements.id"),
        nullable=False
    )

    label = db.Column(
        db.String(50),
        nullable=False
    )

    heure_debut = db.Column(
        db.String(5),
        nullable=False
    )

    heure_fin = db.Column(
        db.String(5),
        nullable=False
    )

    jour = db.Column(
        db.String(20),
        nullable=False
    )

    etablissement = db.relationship(
        "Etablissement",
        backref=db.backref("creneaux", lazy=True)
    )

    def __repr__(self):
        return f"{self.jour} {self.heure_debut}-{self.heure_fin}"
