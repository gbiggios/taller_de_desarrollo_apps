from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
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


