# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    activities = db.relationship('Activity', backref='user', lazy=True)

class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    usuario = db.relationship('User', backref='grupos')

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    horas = db.Column(db.String(8), nullable=False)
    
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)
    grupo = db.relationship('Grupo', backref='actividades')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)