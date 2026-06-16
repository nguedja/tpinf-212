import secrets
import string
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

    code = db.Column(
        db.String(8),
        unique=True,
        nullable=False
    )

    @staticmethod
    def generer_code():
        while True:
            code = ''.join(
                secrets.choice(string.ascii_uppercase + string.digits)
                for _ in range(6)
            )
            if not Etablissement.query.filter_by(code=code).first():
                return code

    def __repr__(self):
        return self.nom
