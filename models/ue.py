from extensions import db


class UE(db.Model):

    __tablename__ = "ues"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    etablissement_id = db.Column(
        db.Integer,
        db.ForeignKey("etablissements.id"),
        nullable=False
    )

    code = db.Column(
        db.String(20),
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

    professeur = db.Column(
        db.String(100),
        nullable=False
    )

    effectif = db.Column(
        db.Integer,
        nullable=False
    )

    besoin_labo = db.Column(
        db.Boolean,
        default=False
    )

    etablissement = db.relationship(
        "Etablissement",
        backref=db.backref("ues", lazy=True)
    )

    def __repr__(self):
        return f"{self.code}"