from flask import Flask, render_template, session
from config import Config
from extensions import db
from routes.ue_routes import ue_bp
from routes.salle_routes import salle_bp
from routes.conflit_routes import conflit_bp
from routes.graphe_routes import graphe_bp
from routes.coloration_routes import coloration_bp
from routes.planning_routes import planning_bp
from routes.etudiant_routes import etudiant_bp
from routes.interdiction_routes import interdiction_bp
from routes.creneau_routes import creneau_bp
from routes.etablissement_routes import etablissement_bp
from routes.regles_routes import regles_bp


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "tpinf212_secret_key_2025"
db.init_app(app)

app.register_blueprint(etablissement_bp)
app.register_blueprint(ue_bp)
app.register_blueprint(salle_bp)
app.register_blueprint(conflit_bp)
app.register_blueprint(graphe_bp)
app.register_blueprint(coloration_bp)
app.register_blueprint(planning_bp)
app.register_blueprint(etudiant_bp)
app.register_blueprint(interdiction_bp)
app.register_blueprint(creneau_bp)
app.register_blueprint(regles_bp)


@app.route("/")
def index():
    from models.etablissement import Etablissement
    etablissements = Etablissement.query.all()
    return render_template(
        "index.html",
        etablissements=etablissements
    )


from models.ue import UE
from models.salle import Salle
from models.conflit import Conflit
from models.etudiant import Etudiant
from models.inscription import Inscription
from models.interdiction import Interdiction
from models.creneau import Creneau
from models.etablissement import Etablissement

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)