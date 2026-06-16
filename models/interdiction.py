from extensions import db


class Interdiction(db.Model):

    __tablename__ = "interdictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    etablissement_id = db.Column(
        db.Integer,
        db.ForeignKey("etablissements.id"),
        nullable=False
    )

    ue1_id = db.Column(
        db.Integer,
        db.ForeignKey("ues.id"),
        nullable=False
    )

    ue2_id = db.Column(
        db.Integer,
        db.ForeignKey("ues.id"),
        nullable=False
    )

    raison = db.Column(
        db.String(200),
        default="Interdiction explicite"
    )

    ue1 = db.relationship(
        "UE",
        foreign_keys=[ue1_id]
    )

    ue2 = db.relationship(
        "UE",
        foreign_keys=[ue2_id]
    )

    etablissement = db.relationship(
        "Etablissement",
        backref=db.backref("interdictions", lazy=True)
    )

    def __repr__(self):
        return f"{self.ue1.code} interdit avec {self.ue2.code}"
