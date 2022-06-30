from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from ..models.entidad.EntidadUsuario import User

from .. import mysql

vistAlumno = Blueprint("vistAlumno", __name__)

@vistAlumno.route("/carrera/materias")
def index():
    cur = mysql.connection.cursor()
    consulta = ("SELECT * FROM materia")
    cur.execute(consulta)
    row = cur.fetchall()
    listMatNom = []
    for column in row:
        listMatNom.append(column[1])
    print(listMatNom)
    return render_template("mostrarMateria.html", user=current_user, row=row)

@vistAlumno.route("/carrera", methods=["GET", "POST"])
def getCarreras():
    cur = mysql.connection.cursor()
    consulta = ('''
SELECT DISTINCT
CarreraNombre as 'Carrera'
FROM
carpo
left JOIN carrera on carpo.CarreraID = carrera.CarreraID
order by CarreraNombre''')
    cur.execute(consulta)
    row = cur.fetchall()
    return render_template("mostrarCarrera.html", user=current_user, row=row)