from flask import Blueprint, request, jsonify
from src import db
from src.models.usuario import Usuario

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    nuevo = Usuario(
        documento=datos['documento'],
        nombre=datos['nombre'],
        email=datos['email'],
        rol=datos.get('rol', 'Vendedor')
    )
    nuevo.set_password(datos['password'])  # Encripta la clave antes de guardar

    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado con éxito", "usuario": nuevo.to_dict()}), 201

@usuario_bp.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios]), 200

@usuario_bp.route('/api/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    datos = request.get_json()
    usuario.documento = datos.get('documento', usuario.documento)
    usuario.nombre = datos.get('nombre', usuario.nombre)
    usuario.email = datos.get('email', usuario.email)
    usuario.rol = datos.get('rol', usuario.rol)
    if 'password' in datos and datos['password']:
        usuario.set_password(datos['password'])

    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado con éxito", "usuario": usuario.to_dict()}), 200

@usuario_bp.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado con éxito"}), 200
