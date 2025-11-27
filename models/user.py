from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

db = TinyDB('database/db.json')
users_table = db.table('users')
UserQuery = Query()

class User:
    def __init__(self, username, email, password=None):
        self.id = str(uuid.uuid4())  # Já converte para string
        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hash = None
        self.created_at = datetime.utcnow().isoformat()
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        users_table.insert(self.to_dict())
    
    def to_dict(self):
        return {
            'id': self.id,  # Já é string
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'created_at': self.created_at
        }
    
    @classmethod
    def find_by_username(cls, username):
        user_data = users_table.get(UserQuery.username == username)
        if user_data:
            return cls.from_dict(user_data)
        return None
    
    @classmethod
    def find_by_id(cls, user_id):
        # Garantir que estamos buscando por string
        user_data = users_table.get(UserQuery.id == str(user_id))
        if user_data:
            return cls.from_dict(user_data)
        return None
    
    @classmethod
    def from_dict(cls, user_data):
        """Cria objeto User a partir de dados do TinyDB"""
        user = cls(user_data['username'], user_data['email'])
        user.id = str(user_data['id'])  # Garante que é string
        user.password_hash = user_data['password_hash']
        user.created_at = user_data['created_at']
        return user
    
    @classmethod
    def create_user(cls, username, email, password):
        """Método auxiliar para criar e salvar usuário"""
        user = cls(username, email, password)
        user.save()
        return user