from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:h6C#UQpRIBOm>H)Y*ugaZvy)~~J)@database-catemuacles.cbq4sgyai27e.us-east-2.rds.amazonaws.com/prueba_1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo DOCENTE
# Modelo DOCENTE
class DOCENTE(db.Model):
    id_docente = db.Column(db.Integer, primary_key=True)
    rut_docente = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    contraseña = db.Column(db.String(50))

# Modelo Sala
class Sala(db.Model):
    id_sala = db.Column(db.Integer, primary_key=True)
    nombre_sala = db.Column(db.String(50), nullable=False)

# Modelo Taller
class Taller(db.Model):
    taller_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id_sala'), nullable=False)
    id_docente = db.Column(db.Integer, db.ForeignKey('docente.id_docente'), nullable=False)

    sala = db.relationship('Sala', backref=db.backref('talleres', lazy=True))
    docente = db.relationship('DOCENTE', backref=db.backref('talleres', lazy=True))

# Modelo Clase
class Clase(db.Model):
    id_clase = db.Column(db.Integer, primary_key=True)
    taller_id = db.Column(db.Integer, db.ForeignKey('taller.taller_id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    comentario_bitacora = db.Column(db.Text)

# Modelo Estudiantes
class Estudiantes(db.Model):
    id_estudiante = db.Column(db.Integer, primary_key=True)
    rut_estudiante = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    curso = db.Column(db.String(20))
    correo_institucional = db.Column(db.String(100))

# Modelo Estudiante_Taller
class EstudianteTaller(db.Model):
    id_taller_estudiante = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiantes.id_estudiante'), nullable=False)
    taller_id = db.Column(db.Integer, db.ForeignKey('taller.taller_id'), nullable=False)

# Modelo Asistencia_Estudiante
class AsistenciaEstudiante(db.Model):
    id_asistencia = db.Column(db.Integer, primary_key=True)
    id_clase = db.Column(db.Integer, db.ForeignKey('clase.id_clase'), nullable=False)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiantes.id_estudiante'), nullable=False)
    presencia = db.Column(db.Boolean, nullable=False)
    justificacion = db.Column(db.Text)

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()#

@app.route('/')
def index():
    return render_template('index.html')

# Rutas y lógica para CRUD de cada modelo
# DOCENTE CRUD
@app.route('/docentes')
def docentes():
    docentes = DOCENTE.query.all()
    return render_template('docentes.html', docentes=docentes)

@app.route('/docente', methods=['POST'])
def create_docente():
    rut_docente = request.form['rut_docente']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')
    
    nuevo_docente = DOCENTE(
        rut_docente=rut_docente,
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        telefono=telefono,
        correo=correo,
        contraseña=contraseña
    )
    
    db.session.add(nuevo_docente)
    db.session.commit()
    return redirect(url_for('docentes'))

@app.route('/docente/<int:id_docente>/delete', methods=['POST'])
def delete_docente(id_docente):
    docente = DOCENTE.query.get_or_404(id_docente)
    db.session.delete(docente)
    db.session.commit()
    return redirect(url_for('docentes'))

@app.route('/docente/<int:id_docente>/edit', methods=['GET'])
def edit_docente(id_docente):
    docente = DOCENTE.query.get_or_404(id_docente)
    return render_template('edit_docente.html', docente=docente)

@app.route('/docente/<int:id_docente>/edit', methods=['POST'])
def update_docente(id_docente):
    docente = DOCENTE.query.get_or_404(id_docente)
    docente.rut_docente = request.form['rut_docente']
    docente.nombre = request.form['nombre']
    docente.apellido_paterno = request.form['apellido_paterno']
    docente.apellido_materno = request.form['apellido_materno']
    docente.telefono = request.form.get('telefono')
    docente.correo = request.form.get('correo')
    docente.contraseña = request.form.get('contraseña')
    
    db.session.commit()
    return redirect(url_for('docentes'))

# Repite lo mismo para las otras tablas (Sala, Taller, Clase, Estudiantes, EstudianteTaller, AsistenciaEstudiante)

# Sala CRUD
@app.route('/salas')
def salas():
    salas = Sala.query.all()
    return render_template('salas.html', salas=salas)

@app.route('/sala', methods=['POST'])
def create_sala():
    nombre_sala = request.form['nombre_sala']
    nueva_sala = Sala(nombre_sala=nombre_sala)
    db.session.add(nueva_sala)
    db.session.commit()
    return redirect(url_for('salas'))

@app.route('/sala/<int:id_sala>/delete', methods=['POST'])
def delete_sala(id_sala):
    sala = Sala.query.get_or_404(id_sala)
    db.session.delete(sala)
    db.session.commit()
    return redirect(url_for('salas'))

@app.route('/sala/<int:id_sala>/edit', methods=['GET'])
def edit_sala(id_sala):
    sala = Sala.query.get_or_404(id_sala)
    return render_template('edit_sala.html', sala=sala)

@app.route('/sala/<int:id_sala>/edit', methods=['POST'])
def update_sala(id_sala):
    sala = Sala.query.get_or_404(id_sala)
    sala.nombre_sala = request.form['nombre_sala']
    db.session.commit()
    return redirect(url_for('salas'))

@app.route('/talleres')
def talleres():
    talleres = Taller.query.all()
    return render_template('talleres.html', talleres=talleres)

@app.route('/taller', methods=['POST'])
def create_taller():
    nombre = request.form['nombre']
    horario = request.form['horario']
    id_sala = request.form['id_sala']
    id_docente = request.form['id_docente']
    
    nuevo_taller = Taller(
        nombre=nombre,
        horario=horario,
        id_sala=id_sala,
        id_docente=id_docente
    )
    
    db.session.add(nuevo_taller)
    db.session.commit()
    return redirect(url_for('talleres'))


@app.route('/taller/<int:taller_id>/delete', methods=['POST'])
def delete_taller(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    db.session.delete(taller)
    db.session.commit()
    return redirect(url_for('talleres'))

@app.route('/taller/<int:taller_id>/edit', methods=['GET'])
def edit_taller(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    return render_template('edit_taller.html', taller=taller)

@app.route('/taller/<int:taller_id>/edit', methods=['POST'])
def update_taller(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    taller.nombre = request.form['nombre']
    taller.horario = request.form['horario']
    taller.id_sala = request.form['id_sala']
    taller.id_docente = request.form['id_docente']
    
    db.session.commit()
    return redirect(url_for('talleres'))

@app.route('/taller/new')
def new_taller():
    docentes = DOCENTE.query.all()  # Obteniendo todos los docentes
    salas = Sala.query.all()  # Obteniendo todas las salas
    return render_template('create_taller.html', docentes=docentes, id_salas=salas)


# Clase CRUD
@app.route('/clases')
def clases():
    clases = Clase.query.all()
    return render_template('clases.html', clases=clases)

@app.route('/clase', methods=['POST'])
def create_clase():
    taller_id = request.form['taller_id']
    fecha = request.form['fecha']
    comentario_bitacora = request.form.get('comentario_bitacora')
    
    nueva_clase = Clase(
        taller_id=taller_id,
        fecha=fecha,
        comentario_bitacora=comentario_bitacora
    )
    
    db.session.add(nueva_clase)
    db.session.commit()
    return redirect(url_for('clases'))

@app.route('/clase/<int:id_clase>/delete', methods=['POST'])
def delete_clase(id_clase):
    clase = Clase.query.get_or_404(id_clase)
    db.session.delete(clase)
    db.session.commit()
    return redirect(url_for('clases'))

@app.route('/clase/<int:id_clase>/edit', methods=['GET'])
def edit_clase(id_clase):
    clase = Clase.query.get_or_404(id_clase)
    return render_template('edit_clase.html', clase=clase)

@app.route('/clase/<int:id_clase>/edit', methods=['POST'])
def update_clase(id_clase):
    clase = Clase.query.get_or_404(id_clase)
    clase.taller_id = request.form['taller_id']
    clase.fecha = request.form['fecha']
    clase.comentario_bitacora = request.form.get('comentario_bitacora')
    
    db.session.commit()
    return redirect(url_for('clases'))

# Estudiantes CRUD
@app.route('/estudiantes')
def estudiantes():
    estudiantes = Estudiantes.query.all()
    return render_template('estudiantes.html', estudiantes=estudiantes)

@app.route('/estudiante', methods=['POST'])
def create_estudiante():
    rut_estudiante = request.form['rut_estudiante']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    curso = request.form.get('curso')
    correo_institucional = request.form.get('correo_institucional')
    
    nuevo_estudiante = Estudiantes(
        rut_estudiante=rut_estudiante,
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        curso=curso,
        correo_institucional=correo_institucional
    )
    
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return redirect(url_for('estudiantes'))

@app.route('/estudiante/<int:id_estudiante>/delete', methods=['POST'])
def delete_estudiante(id_estudiante):
    estudiante = Estudiantes.query.get_or_404(id_estudiante)
    db.session.delete(estudiante)
    db.session.commit()
    return redirect(url_for('estudiantes'))

@app.route('/estudiante/<int:id_estudiante>/edit', methods=['GET'])
def edit_estudiante(id_estudiante):
    estudiante = Estudiantes.query.get_or_404(id_estudiante)
    return render_template('edit_estudiante.html', estudiante=estudiante)

@app.route('/estudiante/<int:id_estudiante>/edit', methods=['POST'])
def update_estudiante(id_estudiante):
    estudiante = Estudiantes.query.get_or_404(id_estudiante)
    estudiante.rut_estudiante = request.form['rut_estudiante']
    estudiante.nombre = request.form['nombre']
    estudiante.apellido_paterno = request.form['apellido_paterno']
    estudiante.apellido_materno = request.form['apellido_materno']
    estudiante.curso = request.form.get('curso')
    estudiante.correo_institucional = request.form.get('correo_institucional')
    
    db.session.commit()
    return redirect(url_for('estudiantes'))

# EstudianteTaller CRUD
@app.route('/estudiantestaller')
def estudiante_talleres():
    estudiante_talleres = EstudianteTaller.query.all()
    return render_template('estudiantestaller.html', estudiante_talleres=estudiante_talleres)

@app.route('/estudiantetaller', methods=['POST'])
def create_estudiante_taller():
    id_estudiante = request.form['id_estudiante']
    taller_id = request.form['taller_id']
    
    nuevo_estudiante_taller = EstudianteTaller(
        id_estudiante=id_estudiante,
        taller_id=taller_id
    )
    
    db.session.add(nuevo_estudiante_taller)
    db.session.commit()
    return redirect(url_for('estudiantestaller'))

@app.route('/estudiantetaller/<int:id_taller_estudiante>/delete', methods=['POST'])
def delete_estudiante_taller(id_taller_estudiante):
    estudiante_taller = EstudianteTaller.query.get_or_404(id_taller_estudiante)
    db.session.delete(estudiante_taller)
    db.session.commit()
    return redirect(url_for('estudiantestaller'))

# AsistenciaEstudiante CRUD
@app.route('/asistenciaestudiantes')
def asistencia_estudiantes():
    asistencias = AsistenciaEstudiante.query.all()
    return render_template('asistenciaestudiantes.html', asistencias=asistencias)

@app.route('/asistenciaestudiante', methods=['POST'])
def create_asistencia_estudiante():
    id_clase = request.form['id_clase']
    id_estudiante = request.form['id_estudiante']
    presencia = request.form.get('presencia')
    justificacion = request.form.get('justificacion')
    
    nueva_asistencia = AsistenciaEstudiante(
        id_clase=id_clase,
        id_estudiante=id_estudiante,
        presencia=presencia,
        justificacion=justificacion
    )
    
    db.session.add(nueva_asistencia)
    db.session.commit()
    return redirect(url_for('asistenciaestudiantes'))

@app.route('/asistenciaestudiante/<int:id_asistencia>/delete', methods=['POST'])
def delete_asistencia_estudiante(id_asistencia):
    asistencia = AsistenciaEstudiante.query.get_or_404(id_asistencia)
    db.session.delete(asistencia)
    db.session.commit()
    return redirect(url_for('asistenciaestudiantes'))


from sqlalchemy import inspect


def tablas_creadas():
    inspector = inspect(db.engine)
    return inspector.get_table_names()

if __name__ == '__main__':
    app.run(debug=True)


# Comprobar si las tablas están creadas antes de crearlas
with app.app_context():
    tablas = tablas_creadas()
    if 'nombre_tabla' not in tablas:
        db.create_all()