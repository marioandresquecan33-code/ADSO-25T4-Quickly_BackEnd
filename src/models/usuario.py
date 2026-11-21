from werkzeug.security import generate_password_hash, check_password_hash
from src import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    documento = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='Vendedor')
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "documento": self.documento,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol
        }
