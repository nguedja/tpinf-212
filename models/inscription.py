from extensions import db


class Inscription(db.Model):

    __tablename__ = "inscriptions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    etudiant_id = db.Column(
        db.Integer,
        db.ForeignKey("etudiants.id"),
        nullable=False
    )

    ue_id = db.Column(
        db.Integer,
        db.ForeignKey("ues.id"),
        nullable=False
    )

    etudiant = db.relationship(
        "Etudiant",
        backref=db.backref("inscriptions", lazy=True)
    )

    ue = db.relationship(
        "UE",
        backref=db.backref("inscriptions", lazy=True)
    )

    def __repr__(self):
        return f"{self.etudiant.matricule} -> {self.ue.code}"
