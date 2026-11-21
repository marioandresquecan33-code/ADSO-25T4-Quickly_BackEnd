from flask import Blueprint, request, jsonify
from src import db
from src.models.factura import Factura, DetalleFactura
from src.models.producto import Producto

factura_bp = Blueprint('factura_bp', __name__)

# CREATE (POST): Registrar una venta y descontar el stock automáticamente
@factura_bp.route('/api/facturas', methods=['POST'])
def crear_factura():
    datos = request.get_json()
    items = datos.get('items', [])

    if not items:
        return jsonify({"error": "La factura debe incluir al menos un producto en 'items'"}), 400

    nueva_factura = Factura(
        cliente_nombre=datos['cliente_nombre'],
        cliente_documento=datos['cliente_documento'],
        total=0.0
    )
    db.session.add(nueva_factura)
    db.session.flush()  # Genera el id_factura sin cerrar aún la transacción

    total_factura = 0.0

    for item in items:
        producto = Producto.query.get(item['id_producto'])
        if not producto:
            db.session.rollback()
            return jsonify({"error": f"El producto con ID {item['id_producto']} no existe"}), 404

        cantidad = int(item['cantidad'])
        if cantidad <= 0:
            db.session.rollback()
            return jsonify({"error": "La cantidad debe ser mayor a cero"}), 400

        # Validar que alcance el inventario disponible
        if producto.stock < cantidad:
            db.session.rollback()
            return jsonify({
                "error": f"Stock insuficiente para '{producto.nombre_producto}'. Disponible: {producto.stock}"
            }), 400

        # Descontar del inventario y calcular subtotal
        producto.stock -= cantidad
        subtotal = producto.precio * cantidad
        total_factura += subtotal

        detalle = DetalleFactura(
            id_factura=nueva_factura.id_factura,
            id_producto=producto.id_producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            subtotal=subtotal
        )
        db.session.add(detalle)

    nueva_factura.total = total_factura
    db.session.commit()

    return jsonify({
        "mensaje": "Factura registrada y stock actualizado con éxito",
        "factura": nueva_factura.to_dict()
    }), 201


# READ (GET): Listar todas las facturas con sus detalles
@factura_bp.route('/api/facturas', methods=['GET'])
def listar_facturas():
    facturas = Factura.query.all()
    return jsonify([f.to_dict() for f in facturas]), 200
