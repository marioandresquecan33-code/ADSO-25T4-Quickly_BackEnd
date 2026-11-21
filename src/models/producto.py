from src import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.String(50), unique=True, nullable=True)
    nombre_producto = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    # Llave foránea conectada a la tabla 'categorias'
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    
    # Relación para poder leer el nombre de la categoría desde el producto
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "barcode": self.barcode,
            "nombre_producto": self.nombre_producto,
            "precio": self.precio,
            "stock": self.stock,
            "id_categoria": self.id_categoria,
            "nombre_categoria": self.categoria.nombre if self.categoria else None
        }
