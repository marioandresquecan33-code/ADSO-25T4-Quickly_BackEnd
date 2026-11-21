from flask import Blueprint, request, jsonify
from src import db
from src.models.cliente import Cliente

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/api/clientes', methods=['POST'])
def crear_cliente():
    datos = request.get_json()
    nuevo = Cliente(
        documento=datos['documento'],
        nombre=datos['nombre'],
        email=datos.get('email'),
        telefono=datos.get('telefono'),
        direccion=datos.get('direccion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Cliente creado con éxito", "cliente": nuevo.to_dict()}), 201

@cliente_bp.route('/api/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes]), 200

@cliente_bp.route('/api/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    datos = request.get_json()
    cliente.documento = datos.get('documento', cliente.documento)
    cliente.nombre = datos.get('nombre', cliente.nombre)
    cliente.email = datos.get('email', cliente.email)
    cliente.telefono = datos.get('telefono', cliente.telefono)
    cliente.direccion = datos.get('direccion', cliente.direccion)

    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado con éxito", "cliente": cliente.to_dict()}), 200

@cliente_bp.route('/api/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado con éxito"}), 200
