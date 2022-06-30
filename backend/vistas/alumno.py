from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from ..models.entidad.EntidadUsuario import User

from .. import mysql

vistAlumno = Blueprint("vistAlumno", __name__)


@vistAlumno.route("/carrera", methods=["GET", "POST"])
@login_required
def getCarreras():
    cur = mysql.connection.cursor()
    consulta = ('SELECT * FROM carrera order by carreranombre')
    cur.execute(consulta)
    row = cur.fetchall()
    return render_template("mostrarCarrera.html", row=row)


@vistAlumno.route("/carrera/<int:idcar>/plan", methods=["GET", "POST"])
@login_required
def getplan(idcar):    
    cur = mysql.connection.cursor()
    consulta = ('''
SELECT
carpo.plandeestudioid,
plandeestudio.plannombre,
carrera.carreraid,
carrera.carreranombre,
carpoid
FROM
carpo
left JOIN carrera on carpo.CarreraID = carrera.CarreraID
left JOIN plandeestudio on carpo.plandeestudioid = plandeestudio.PlanID
where carrera.carreraid = %s
order by CarreraNombre
''')
    cur.execute(consulta,([idcar]))
    row = cur.fetchall()
    return render_template("mostrarPlanes.html", row=row)

@vistAlumno.route("/carrera/<int:idcar>/plan/<int:idplan>/carpo/<int:idcarpo>/materias")
@login_required
def getMateriasCarreraPlanID(idcar, idplan, idcarpo):
    cur = mysql.connection.cursor()
    consulta = ("SELECT * FROM materia where idcarpo = %s")
    cur.execute(consulta,([idcarpo]))
    row = cur.fetchall()
    return render_template("mostrarMateria.html", row=row)


@vistAlumno.route("/mostrarCarrerasInscriptas")
@login_required
def getCarrerasInscriptas():
    # Se optiene la ID del Usuario
    iduser = current_user.id
    
    #Primero se pasa por el Perfil del Usuario
    cur = mysql.connection.cursor()
    consulta = ("SELECT idusuarioperfil from usuariosperfiles where idusuario = %s")
    cur.execute(consulta,[(iduser)])
    iduser = cur.fetchone()[0]

    #Segundo se pasa por el Estudiante
    consulta = ("SELECT idestudiante from estudiante where IDusuariosPerfiles = %s")
    cur.execute(consulta,[(iduser)])
    iduser = cur.fetchone()[0]

    #Tercero se pasa por el CarpoEstudiante
    consulta = ("SELECT idCarpo, idCarpoEstudiante from CarpoEstudiante where idestudiante = %s")
    cur.execute(consulta,[(iduser)])
    auxiliar = cur.fetchone()
    Carpo = auxiliar[0]
    iduser = auxiliar[1]
    
    #Cuarto, se revisa que Carrera es
    consulta = ('''SELECT DISTINCT
CarreraNombre as 'Carrera',
PlanNombre as 'Plan',
IFNULL(OrientacionNombre,'Sin Orientación') as 'Orientación'
FROM
carpo
left JOIN carrera on carpo.CarreraID = carrera.CarreraID
left JOIN plandeestudio on carpo.PlanDeEstudioID = plandeestudio.PlanID
left join orientacion on carpo.orientacionid = orientacion.orientacionid
where carpoid = %s
order by CarreraNombre;
''')
    cur.execute(consulta,[(Carpo)])
    row = cur.fetchone()
    
    #Quinto, se revisa que Materias esta inscripto
    consulta = ('select idmateria from carpestmateria where idcarpoestudiante = %s')
    cur.execute(consulta, [(iduser)])
    listaMateriasObtenidas = cur.fetchone()
    return render_template("mostrarCarreraInscripta.html",rowcarpo=row, listamaterias=listaMateriasObtenidas)



@vistAlumno.route("/mostrarCarrerasInscriptas/<materias>/Materias")
@login_required
def getMateriasInscriptas(materias):
    listaMaterias = []
    materias = materias.replace('(','').replace(')','').replace('[','').replace(']','').replace(',','')
    materias = materias.split(' ')
    for materia in materias:
        cur = mysql.connection.cursor()
        consulta = ('SELECT nombremateria, tipo from materia where idmateria = %s')
        cur.execute(consulta, [(str(materia))])
        row = cur.fetchone()
        materias.append(row)
        listaMaterias.append(materias)
    print(listaMaterias)
    
    
    return render_template("mostrarMateriasInscriptas.html")