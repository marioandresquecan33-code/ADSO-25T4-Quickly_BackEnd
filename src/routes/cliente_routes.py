from flask import Blueprint, request, jsonify
from src import db
from src.models.cliente import Cliente

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/api/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    resultado = [
        {
            "id_cliente": c.id_cliente,
            "documento": c.documento,
            "nombre": c.nombre,
            "email": c.email,
            "telefono": c.telefono,
            "direccion": c.direccion
        }
        for c in clientes
    ]
    return jsonify(resultado), 200

@cliente_bp.route('/api/clientes', methods=['POST'])
def crear_cliente():
    data = request.get_json()
    if not data or not data.get('documento') or not data.get('nombre'):
        return jsonify({"error": "El documento y el nombre son obligatorios."}), 400

    documento = str(data['documento']).strip()
    nombre = str(data['nombre']).strip()

    existente = Cliente.query.filter_by(documento=documento).first()
    if existente:
        if existente.nombre.strip().lower() != nombre.lower():
            return jsonify({
                "error": f"La cédula {documento} ya está registrada a nombre de '{existente.nombre}'. No se permite registrarla con otro nombre."
            }), 400
        return jsonify({
            "error": f"El cliente con cédula {documento} ya se encuentra registrado."
        }), 400

    email = data.get('email', '').strip() if data.get('email') else None
    if email and Cliente.query.filter_by(email=email).first():
        return jsonify({"error": f"El correo {email} ya está registrado con otro cliente."}), 400

    nuevo_cliente = Cliente(
        documento=documento,
        nombre=nombre,
        email=email,
        telefono=data.get('telefono'),
        direccion=data.get('direccion')
    )
    db.session.add(nuevo_cliente)
    db.session.commit()

    return jsonify({
        "mensaje": "Cliente registrado exitosamente",
        "id_cliente": nuevo_cliente.id_cliente
    }), 201

@cliente_bp.route('/api/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    nuevo_doc = str(data.get('documento', cliente.documento)).strip()
    nuevo_nombre = str(data.get('nombre', cliente.nombre)).strip()

    otro = Cliente.query.filter(Cliente.documento == nuevo_doc, Cliente.id_cliente != id).first()
    if otro:
        return jsonify({
            "error": f"La cédula {nuevo_doc} ya pertenece a '{otro.nombre}'."
        }), 400

    cliente.documento = nuevo_doc
    cliente.nombre = nuevo_nombre
    cliente.email = data.get('email', cliente.email)
    cliente.telefono = data.get('telefono', cliente.telefono)
    cliente.direccion = data.get('direccion', cliente.direccion)

    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado correctamente"}), 200

@cliente_bp.route('/api/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado correctamente"}), 200
