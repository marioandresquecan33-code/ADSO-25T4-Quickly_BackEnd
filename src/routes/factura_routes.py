from flask import Blueprint, request, jsonify
from src import db
from src.models.factura import Factura, DetalleFactura
from src.models.producto import Producto
from src.models.cliente import Cliente

factura_bp = Blueprint('factura_bp', __name__)

# Listar historial de facturas con detalle
@factura_bp.route('/api/facturas', methods=['GET'])
def listar_facturas():
    facturas = Factura.query.order_by(Factura.id_factura.desc()).all()
    resultado = []
    for f in facturas:
        detalles_lista = []
        for d in f.detalles:
            detalles_lista.append({
                "id_producto": d.id_producto,
                "nombre_producto": d.producto.nombre_producto if d.producto else "Producto eliminado",
                "cantidad": d.cantidad,
                "precio_unitario": float(d.precio_unitario),
                "subtotal": float(d.subtotal)
            })
        resultado.append({
            "id_factura": f.id_factura,
            "fecha": f.fecha.strftime("%Y-%m-%d %H:%M:%S") if f.fecha else "",
            "cliente_nombre": f.cliente_nombre,
            "cliente_documento": f.cliente_documento,
            "total": float(f.total),
            "detalles": detalles_lista
        })
    return jsonify(resultado), 200

# Emitir factura con validación de cédula/nombre y descuento automático de stock
@factura_bp.route('/api/facturas', methods=['POST'])
def crear_factura():
    data = request.get_json()
    if not data or not data.get('cliente_documento') or not data.get('cliente_nombre'):
        return jsonify({"error": "El documento y nombre del cliente son obligatorios."}), 400

    items = data.get('items', [])
    if not items:
        return jsonify({"error": "Debe incluir al menos un producto en la factura."}), 400

    doc_cliente = str(data['cliente_documento']).strip()
    nom_cliente = str(data['cliente_nombre']).strip()

    # Validación: Si la cédula ya existe en la tabla clientes, el nombre DEBE coincidir
    cliente_registrado = Cliente.query.filter_by(documento=doc_cliente).first()
    if cliente_registrado and cliente_registrado.nombre.strip().lower() != nom_cliente.lower():
        return jsonify({
            "error": f"Error de validación: la cédula {doc_cliente} ya está registrada a nombre de '{cliente_registrado.nombre}', no de '{nom_cliente}'."
        }), 400

    # Validar existencia y stock de todos los productos antes de guardar
    total_factura = 0
    detalles_a_guardar = []

    for item in items:
        producto = Producto.query.get(item.get('id_producto'))
        cantidad = int(item.get('cantidad', 0))

        if not producto:
            return jsonify({"error": f"El producto con ID {item.get('id_producto')} no existe."}), 404
        if cantidad <= 0:
            return jsonify({"error": "La cantidad debe ser mayor a cero."}), 400
        if producto.stock < cantidad:
            return jsonify({
                "error": f"Stock insuficiente para '{producto.nombre_producto}'. Disponible: {producto.stock}, solicitado: {cantidad}."
            }), 400

        subtotal = float(producto.precio) * cantidad
        total_factura += subtotal
        detalles_a_guardar.append((producto, cantidad, float(producto.precio), subtotal))

    # Crear factura y descontar stock
    nueva_factura = Factura(
        cliente_nombre=nom_cliente,
        cliente_documento=doc_cliente,
        total=total_factura
    )
    db.session.add(nueva_factura)
    db.session.flush()

    for producto, cantidad, precio_unit, subtotal in detalles_a_guardar:
        producto.stock -= cantidad
        detalle = DetalleFactura(
            id_factura=nueva_factura.id_factura,
            id_producto=producto.id_producto,
            cantidad=cantidad,
            precio_unitario=precio_unit,
            subtotal=subtotal
        )
        db.session.add(detalle)

    db.session.commit()

    return jsonify({
        "mensaje": "Factura emitida y stock descontado correctamente",
        "id_factura": nueva_factura.id_factura,
        "total": total_factura
    }), 201
