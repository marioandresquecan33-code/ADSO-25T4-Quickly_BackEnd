# Quickly BackEnd - API REST de Administración y Facturación

API RESTful desarrollada en **Python (Flask)** y **MySQL (SQLAlchemy)** para gestionar la lógica de negocio, persistencia de datos, control automático de inventario y seguridad de credenciales del sistema de facturación electrónica **Quickly**.

---

## 🏗️ Arquitectura del Proyecto

Este servicio opera bajo una **arquitectura cliente-servidor desacoplada**, exponiendo endpoints en formato JSON en el puerto `5002` para ser consumidos por el Frontend web o clientes HTTP como Postman.

```text
ADSO-25T4-Quickly_BackEnd/
├── src/
│   ├── __init__.py              # Inicialización de Flask, SQLAlchemy y Blueprints
│   ├── app.py                   # Punto de entrada del servidor (Puerto 5002)
│   ├── models/                  # Modelos relacionales ORM (6 tablas en MySQL)
│   │   ├── categoria.py         # Tabla: categorias
│   │   ├── producto.py          # Tabla: productos (FK id_categoria)
│   │   ├── cliente.py           # Tabla: clientes
│   │   ├── usuario.py           # Tabla: usuarios (con hash de contraseñas)
│   │   ├── factura.py           # Tabla: facturas
│   │   └── detalle_factura.py   # Tabla: detalle_facturas (FK id_factura, id_producto)
│   └── routes/                  # Controladores / Endpoints REST
│       ├── categoria_routes.py
│       ├── producto_routes.py
│       ├── cliente_routes.py
│       ├── usuario_routes.py
│       └── factura_routes.py
└── README.md
```

---

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Framework Web:** Flask
* **ORM y Base de Datos:** Flask-SQLAlchemy, PyMySQL, MySQL (XAMPP / phpMyAdmin)
* **Seguridad:** Werkzeug Security (`generate_password_hash` / `check_password_hash`)

---

## 🚀 Guía de Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com
   cd ADSO-25T4-Quickly_BackEnd
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate   # En Windows (Git Bash)
   ```

3. **Instalar dependencias:**
   ```bash
   pip install flask flask-sqlalchemy pymysql werkzeug
   ```

4. **Configurar la base de datos:**
   * Iniciar el servicio **MySQL** en el Panel de Control de XAMPP.
   * Crear una base de datos vacía llamada **`quickly_db`** en phpMyAdmin (las 6 tablas se generan automáticamente al iniciar la aplicación).

5. **Ejecutar el servidor API:**
   ```bash
   python -m src.app
   ```
   El servidor quedará disponible en: `http://127.0.0.1:5002`

---

## 📡 Documentación de Endpoints (API REST)

### Categorías

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/categorias` | Lista todas las categorías registradas |
| `POST` | `/api/categorias` | Crea una nueva categoría (`nombre`, `descripcion`) |
| `PUT` | `/api/categorias/<id>` | Actualiza una categoría existente |
| `DELETE` | `/api/categorias/<id>` | Elimina una categoría por ID |

### Productos

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/productos` | Lista productos con el nombre de su categoría asociada |
| `POST` | `/api/productos` | Registra un producto (`barcode`, `nombre_producto`, `precio`, `stock`, `id_categoria`) |
| `PUT` | `/api/productos/<id>` | Actualiza precio, stock o datos de un producto |
| `DELETE` | `/api/productos/<id>` | Elimina un producto por ID |

### Clientes

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/clientes` | Lista todos los clientes registrados |
| `POST` | `/api/clientes` | Registra un nuevo cliente (`documento`, `nombre`, `email`, `telefono`, `direccion`) |
| `PUT` | `/api/clientes/<id>` | Actualiza la información de un cliente |
| `DELETE` | `/api/clientes/<id>` | Elimina un cliente por ID |

### Usuarios y Autenticación

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/usuarios` | Lista los usuarios del sistema (sin exponer contraseñas) |
| `POST` | `/api/usuarios` | Registra un usuario encriptando su contraseña (`password_hash`) |
| `PUT` | `/api/usuarios/<id>` | Actualiza datos o rol de un usuario |
| `DELETE` | `/api/usuarios/<id>` | Elimina un usuario por ID |
| `POST` | `/api/login` | Valida `email` y `password` contra el hash guardado en MySQL |

### Facturación y Control de Inventario

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/facturas` | Consulta el historial de facturas con su detalle de ítems |
| `POST` | `/api/facturas` | Emite una factura, valida stock disponible, calcula totales y **descuenta inventario automáticamente** |

---

## 👨‍💻 Autor
**Mario Andrés Quecán Velásquez**  
Tecnólogo en Análisis y Desarrollo de Software (ADSO) Ficha 3336128 - SENA

