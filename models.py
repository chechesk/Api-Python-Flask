# models.py
from sqlalchemy import Column, Integer, String
from config import Base
import bcrypt

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False)  # Almacenamos el hash en lugar de la contraseña

    # Método para establecer el hash de la contraseña
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    # Método para verificar la contraseña
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))