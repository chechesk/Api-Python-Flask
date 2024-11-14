from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy.orm import Session
from config import SessionLocal, engine
from models import Base, Usuario
from asgiref.wsgi import WsgiToAsgi
from flask_cors import CORS

# Crear la base de datos
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

CORS(app, resources={
    r"/*": {
        "origins": ["http://www.tradingpro.ai"],
        "methods": ["GET", "POST", "DELETE", "PUT", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# ---------------Ruta principal---------------------
@app.route("/", methods=['GET'])
def read_root():
    return {"Mensaje": "¡Bienvenido a APIPYTHON!"}

# Obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    with SessionLocal() as db:
        usuarios = db.query(Usuario).all()
        return jsonify([{"id": u.id, "nombre": u.nombre, "email": u.email} for u in usuarios]), 200

# Obtener un usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    with SessionLocal() as db:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if usuario:
            return jsonify({"id": usuario.id, "nombre": usuario.nombre, "email": usuario.email}), 200
        return jsonify({"error": "Usuario no encontrado"}), 404

# Crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    try:   
        datos = request.get_json()
        nuevo_usuario = Usuario(nombre=datos["nombre"], email=datos["email"])
        nuevo_usuario.set_password(datos["password"])  # Hashea la contraseña usando set_password

        with SessionLocal() as db:
            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)

        return jsonify({
    "mensaje": "Correo registrado exitosamente",
    "id": nuevo_usuario.id,
    "nombre": nuevo_usuario.nombre,
    "email": nuevo_usuario.email
}), 201

    except sqlalchemy.exc.IntegrityError as e:
        # Error de duplicidad (por ejemplo, el email ya existe)
        app.logger.error(f"Error de integridad en la base de datos: {str(e)}")
        return jsonify({"error": "El email ya está registrado"}), 400
    except Exception as e:
        # Error genérico
        app.logger.error(f"Error al crear usuario: {str(e)}")
        return jsonify({"error": "Ocurrió un error al crear el usuario"}), 500


# Actualizar un usuario existente
@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    with SessionLocal() as db:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if usuario:
            datos = request.get_json()
            usuario.nombre = datos["nombre"]
            usuario.email = datos["email"]
            db.commit()
            return jsonify({"id": usuario.id, "nombre": usuario.nombre, "email": usuario.email}), 200
        return jsonify({"error": "Usuario no encontrado"}), 404

# Eliminar un usuario
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    with SessionLocal() as db:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return jsonify({"mensaje": "Usuario eliminado"}), 200
        return jsonify({"error": "Usuario no encontrado"}), 404
    
@app.route('/login', methods=['POST'])
def login():
    with SessionLocal() as db:
        datos = request.get_json()
        usuario = db.query(Usuario).filter(Usuario.email == datos["email"]).first()
        if usuario and usuario.verify_password(datos["password"]):
            return jsonify({"mensaje": "Autenticación exitosa"}), 200
        return jsonify({"error": "Credenciales incorrectas"}), 401

# Manejo de error 404 (Página no encontrada)
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Página no encontrada", "message": str(error)}), 404

# Manejo de error 500 (Error interno del servidor)
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor", "message": str(error)}), 500

# Manejo de errores generales (Excepciones no manejadas)
@app.errorhandler(Exception)
def handle_exception(error):
    # Si el error tiene un código de estado, lo usamos, si no, asumimos que es un error 500.
    code = getattr(error, "code", 500)
    return jsonify({"error": "Error no manejado", "message": str(error)}), code
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host="localhost", port=8000, log_level="info")
