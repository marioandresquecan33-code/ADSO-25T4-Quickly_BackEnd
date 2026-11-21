from datetime import datetime
from src import db

class Factura(db.Model):
    __tablename__ = 'facturas'

    id_factura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    cliente_nombre = db.Column(db.String(120), nullable=False)
    cliente_documento = db.Column(db.String(30), nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)

    # Relación maestro-detalle con la tabla 'detalle_facturas'
    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_factura": self.id_factura,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "cliente_nombre": self.cliente_nombre,
            "cliente_documento": self.cliente_documento,
            "total": self.total,
            "detalles": [d.to_dict() for d in self.detalles]
        }


class DetalleFactura(db.Model):
    __tablename__ = 'detalle_facturas'

    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('facturas.id_factura'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Relación para mostrar el nombre del producto vendido en el JSON
    producto = db.relationship('Producto')

    def to_dict(self):
        return {
            "id_detalle": self.id_detalle,
            "id_producto": self.id_producto,
            "nombre_producto": self.producto.nombre_producto if self.producto else None,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal
        }
