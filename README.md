# Api Python Flask
API Monolítica con Flask
Esta es una API monolítica desarrollada en Python utilizando el framework Flask. Esta API permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre los recursos de usuarios y también cuenta con un endpoint de autenticación.

Configuración
Variables de Entorno
Es necesario configurar un archivo .env con las siguientes variables para que la aplicación se conecte correctamente a la base de datos:

plaintext
Copiar código
DATABASE_HOST=your_database_host
DATABASE_PORT=your_database_port
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_NAME=your_database_name
Instalación
Clonar el repositorio:

bash
Copiar código
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
Crear y activar un entorno virtual (opcional pero recomendado):

bash
Copiar código
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Instalar las dependencias:

bash
Copiar código
pip install -r requirements.txt
Configurar el archivo .env con las variables necesarias para la conexión a la base de datos.

Iniciar la aplicación:

bash
Copiar código
flask run --host=0.0.0.0 --port=8000
La API estará disponible en http://localhost:8000.

Endpoints
Ruta Principal
GET /

Devuelve un mensaje de bienvenida o información de la API.
Obtener todos los usuarios
GET /usuarios

Devuelve una lista de todos los usuarios.
Obtener un usuario por ID
GET /usuarios/<int:id>

Devuelve los detalles de un usuario específico basado en el ID.
Crear un nuevo usuario
POST /usuarios

Crea un nuevo usuario con los datos proporcionados en el cuerpo de la solicitud.
Actualizar un usuario existente
PUT /usuarios/<int:id>

Actualiza la información de un usuario existente con el ID especificado.
Eliminar un usuario
DELETE /usuarios/<int:id>

Elimina un usuario basado en el ID especificado.
Iniciar sesión
POST /login

Autenticación de usuario.
Configuración CORS
Se ha habilitado CORS en la aplicación para permitir solicitudes desde cualquier origen y los siguientes métodos HTTP: GET, POST, DELETE, PUT, PATCH. Además, permite los encabezados Content-Type y Authorization.

python
Copiar código
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "DELETE", "PUT", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
Ejecución de Pruebas
Para ejecutar pruebas (si están disponibles), puedes ejecutar el siguiente comando:

bash
Copiar código
pytest
