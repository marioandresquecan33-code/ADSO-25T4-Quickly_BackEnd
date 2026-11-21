from src import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    documento = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "documento": self.documento,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion
        }
