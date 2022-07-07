import os

from ..funcionalidades import helperfecha

from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from ..models.entidad.EntidadUsuario import User

from .. import mysql

#Template folder
template_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'frontend', 'templates','alumno'))

vistAlumno = Blueprint("vistAlumno", __name__,template_folder=template_dir)

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
    carrera = request.args.get('carrera')
    print(carrera)
    
    cur = mysql.connection.cursor()
    consulta = ("SELECT * FROM materia where idcarpo = %s")
    cur.execute(consulta,([idcarpo]))
    row = cur.fetchall()

    año=0
    for mat in row:
        for i in range(4):
            if int(mat[3])>año:
                año=int(mat[3])

    años = [['Primer Año','1'],['Segundo Año','2'],['Tercer Año','3'],['Cuarto Año','4'],['Quinto Año','5']]
    #cur.execute('SELECT carreraId FROM carpo WHERE carpoid = %s',([idcarpo]))
    #carreraId = int(cur.fetchone()[0])
    #cur.execute('SELECT año FROM carrera WHERE carreraid = %s',([carreraId]))
    #año = int(cur.fetchone()[0])
    return render_template("mostrarMateria.html", row=row, años = años, año = año, carrera=carrera)


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

    # #Cuarto, se revisa que Carrera es
    consulta = ('''SELECT DISTINCT CarreraNombre as 'Carrera', PlanNombre as 'Plan', 
IFNULL(OrientacionNombre,'Sin Orientación') as 'Orientación', idCARPOEstudiante 
FROM carpo left JOIN carrera on carpo.CarreraID = carrera.CarreraID 
left JOIN plandeestudio on carpo.PlanDeEstudioID = plandeestudio.PlanID 
left join orientacion on carpo.orientacionid = orientacion.orientacionid 
inner join carpoestudiante on carpoestudiante.idcarpo = carpo.carpoid where carpoestudiante.idestudiante = %s order by CarreraNombre''')

    cur.execute(consulta,[iduser])
    row=cur.fetchall()
    return render_template("mostrarCarreraInscripta.html",rowcarpo=row)



@vistAlumno.route("/mostrarCarrerasInscriptas/Materias")
@login_required
def getMateriasInscriptas():
    cur = mysql.connection.cursor()
    idcarpos = request.args.get('idcarpo')
    carrera = request.args.get('carrera')
    
    consulta = ('select idmateria from carpestmateria where idcarpoestudiante = %s')
    cur.execute(consulta, [(idcarpos)])
    materias = str(cur.fetchall()).replace('(','').replace(')','').replace(',','').split(' ')
    listaMaterias = []
    try:
        for materia in materias:
            cur = mysql.connection.cursor()
            consulta = ('SELECT * from materia where idmateria = %s')
            cur.execute(consulta, [(str(materia))])
            row = cur.fetchone()
            listaMaterias.append(row)
        año=0
        for mat in listaMaterias:
            for i in range(4):
                if int(mat[3])>año:
                    año=int(mat[3])
    except Exception as ex:
        return render_template("mostrarMateriasInscriptas.html",materias=[],años=[], año=-1)

    años = [['Primer Año','1'],['Segundo Año','2'],['Tercer Año','3'],['Cuarto Año','4'],['Quinto Año','5']]
    return render_template("mostrarMateriasInscriptas.html",materias=listaMaterias,años=años, año=año,carrera=carrera)


@vistAlumno.route("/inscripcionExamen", methods=['GET','POST'])
@login_required
def inscribirseExamen():
    añoActual = helperfecha.añoActual
    
    mesActual = helperfecha.mesActual
    mesSiguiente = helperfecha.mesSiguiente
    
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        consulta = '''SELECT
materia.nombremateria, materia.año,
mesaexamenes.fechaExamen, mesaexamenes.modoexamen
from mesaexamenes
inner join materia on materia.idmateria = mesaexamenes.idmateria
inner join calendario_has_mesaexamenes on calendario_has_mesaexamenes.mesaexamenes_idMesaExamenes = mesaexamenes.idmesaexamenes
inner join calendario on calendario.idcalendario = calendario_has_mesaexamenes.calendario_idcalendario
where calendario_has_mesaexamenes.vigenciaexamen = 1
and calendario.fecha_desde >= '%s-%s-01 00:00:00' and calendario.fecha_hasta <= '%s-%s-01 00:00:00'
'''
        cur.execute(consulta,(añoActual,mesActual,añoActual, mesSiguiente))
        row = cur.fetchall()
        print(row)
    
    return render_template("inscripcionExamenes.html",rowExamenes = row)