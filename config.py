import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "projet_examens_l2_2026"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "database", "examens.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False