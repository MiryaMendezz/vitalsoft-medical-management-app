from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    tipo_sangre = db.Column(db.String(5), nullable=True)
    edad = db.Column(db.Integer, nullable=True)
    ultima_consulta = db.Column(db.DateTime, nullable=True)
    motivo_consulta = db.Column(db.String(255), nullable=True)
    citas = db.relationship('Cita', backref='paciente', lazy=True)
    historias = db.relationship('HistoriaClinica', backref='paciente', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    estado = db.Column(db.String(20), default='Activo')
    citas = db.relationship('Cita', backref='doctor', lazy=True)
    historias = db.relationship('HistoriaClinica', backref='doctor', lazy=True)

class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctores.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.String(20), default='Programada')

class HistoriaClinica(db.Model):
    __tablename__ = 'historias_clinicas'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctores.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descripcion = db.Column(db.Text, nullable=False)
    medicamentos = db.Column(db.Text)  # Lista de medicamentos recetados
    diagnostico = db.Column(db.Text)
    tratamiento = db.Column(db.Text)

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    stock = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=10)
    estado = db.Column(db.String(20), default='Disponible')

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), default='admin')
