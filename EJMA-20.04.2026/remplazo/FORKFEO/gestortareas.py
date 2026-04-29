from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from datetime import datetime
import bcrypt 

class GestorTareas:
    def __init__(self, uri: str):
        """Inicializar conexión a MongoDB Atlas"""
        try:
            self.cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.cliente.admin.command('ping')
            self.db = self.cliente['24308060610017']
            self.tareas = self.db['tareas']
            self.usuarios = self.db['usuarios']
            
            self.usuarios.create_index("gmail", unique=True)
            print("✅ Conexión exitosa a MongoDB desde el módulo")
        except ConnectionFailure:
            print("❌ Error: No se pudo conectar a MongoDB")
            raise

    def crear_usuario(self, nombre, gmail, contraseña, razon):
        try:
            salt = bcrypt.gensalt()
            password_hashed = bcrypt.hashpw(contraseña.encode('utf-8'), salt)

            datos_usuario = {
                "nombre": nombre,
                "gmail": gmail,
                "contraseña": password_hashed, 
                "razon": razon,
                "fecha_registro": datetime.now(),
                "activo": True
            }
            resultado = self.usuarios.insert_one(datos_usuario)
            return str(resultado.inserted_id)
        except DuplicateKeyError:
            print(f"❌ El email {gmail} ya existe.")
            return None
        
    def obtener_usuario_por_gmail(self, gmail):
        """Busca un usuario en la base de datos por su correo"""
        try:
            usuario = self.usuarios.find_one({"gmail": gmail})
            return usuario  
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None
