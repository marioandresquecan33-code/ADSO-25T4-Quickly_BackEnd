from flask import Blueprint, request, jsonify
from src import db
from src.models.categoria import Categoria

categoria_bp = Blueprint('categoria_bp', __name__)

# CREATE (POST): Crear una nueva categoría
@categoria_bp.route('/api/categorias', methods=['POST'])
def crear_categoria():
    datos = request.get_json()
    nueva = Categoria(
        nombre=datos['nombre'],
        descripcion=datos.get('descripcion', '')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Categoría creada con éxito", "categoria": nueva.to_dict()}), 201

# READ (GET): Listar todas las categorías
@categoria_bp.route('/api/categorias', methods=['GET'])
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias]), 200

# UPDATE (PUT): Actualizar una categoría existente por su ID
@categoria_bp.route('/api/categorias/<int:id>', methods=['PUT'])
def actualizar_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404

    datos = request.get_json()
    categoria.nombre = datos.get('nombre', categoria.nombre)
    categoria.descripcion = datos.get('descripcion', categoria.descripcion)

    db.session.commit()
    return jsonify({"mensaje": "Categoría actualizada con éxito", "categoria": categoria.to_dict()}), 200

# DELETE (DELETE): Eliminar una categoría por su ID
@categoria_bp.route('/api/categorias/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404

    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"mensaje": "Categoría eliminada con éxito"}), 200


