from extensions import db


class Conflit(db.Model):

    __tablename__ = "conflits"

    id = db.Column(
        db.Integer,
        primary_key=True
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

    ue1 = db.relationship(
        "UE",
        foreign_keys=[ue1_id]
    )

    ue2 = db.relationship(
        "UE",
        foreign_keys=[ue2_id]
    )

    def __repr__(self):
        return f"{self.ue1_id} - {self.ue2_id}"