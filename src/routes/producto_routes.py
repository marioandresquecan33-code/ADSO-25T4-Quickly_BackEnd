from flask import Blueprint, request, jsonify
from src import db
from src.models.producto import Producto
from src.models.categoria import Categoria

producto_bp = Blueprint('producto_bp', __name__)

# CREATE (POST): Crear un producto asociado a una categoría existente
@producto_bp.route('/api/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()

    # Verificar que la categoría exista antes de guardar el producto
    categoria = Categoria.query.get(datos['id_categoria'])
    if not categoria:
        return jsonify({"error": "La categoría indicada no existe"}), 404

    nuevo = Producto(
        barcode=datos.get('barcode'),
        nombre_producto=datos['nombre_producto'],
        precio=float(datos['precio']),
        stock=int(datos.get('stock', 0)),
        id_categoria=int(datos['id_categoria'])
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Producto creado con éxito", "producto": nuevo.to_dict()}), 201

# READ (GET): Listar todos los productos
@producto_bp.route('/api/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos]), 200

# UPDATE (PUT): Actualizar un producto por su ID
@producto_bp.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    datos = request.get_json()
    if 'id_categoria' in datos:
        categoria = Categoria.query.get(datos['id_categoria'])
        if not categoria:
            return jsonify({"error": "La categoría indicada no existe"}), 404
        producto.id_categoria = int(datos['id_categoria'])

    producto.barcode = datos.get('barcode', producto.barcode)
    producto.nombre_producto = datos.get('nombre_producto', producto.nombre_producto)
    if 'precio' in datos:
        producto.precio = float(datos['precio'])
    if 'stock' in datos:
        producto.stock = int(datos['stock'])

    db.session.commit()
    return jsonify({"mensaje": "Producto actualizado con éxito", "producto": producto.to_dict()}), 200

# DELETE (DELETE): Eliminar un producto por su ID
@producto_bp.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    db.session.delete(producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado con éxito"}), 200
