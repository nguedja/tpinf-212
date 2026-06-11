from routes.coloration_routes import coloration_bp
from routes.conflit_routes import conflit_bp
from routes.graphe_routes import graphe_bp
from flask import Flask, render_template
from config import Config
from extensions import db
from routes.ue_routes import ue_bp
from routes.salle_routes import salle_bp
from routes.planning_routes import planning_bp


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(ue_bp)
app.register_blueprint(salle_bp)
app.register_blueprint(conflit_bp)
app.register_blueprint(graphe_bp)
app.register_blueprint(coloration_bp)
app.register_blueprint(planning_bp)

db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ues")
def ues():
    return "<h2>Page UE en construction</h2>"


@app.route("/salles")
def salles():
    return "<h2>Page Salles en construction</h2>"


@app.route("/graphe")
def graphe():
    return "<h2>Page Graphe en construction</h2>"


@app.route("/planning")
def planning():
    return "<h2>Page Planning en construction</h2>"


from models.ue import UE
from models.salle import Salle
from models.conflit import Conflit

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)