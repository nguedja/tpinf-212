from flask import (
    Blueprint,
    render_template
)

regles_bp = Blueprint(
    "regles",
    __name__
)


@regles_bp.route("/regles")
def regles():
    return render_template("regles.html")
