from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from ..models.entidad.EntidadUsuario import User

views = Blueprint("views", __name__)

@views.route("/")
def index():
<<<<<<< HEAD
    return render_template("home.html", user=current_user)
=======
    return render_template("home.html")
>>>>>>> 7f87bf5 (Merge branch 'master' of https://github.com/berseKIEL/ProjectoFLASKISPP)

@views.route("/home")
@login_required
def home():
    flash('Se inicio la sesion!', category='success')
<<<<<<< HEAD
    return render_template("homeAlumno.html")
=======
    return render_template("homeInicio.html")
>>>>>>> 7f87bf5 (Merge branch 'master' of https://github.com/berseKIEL/ProjectoFLASKISPP)
