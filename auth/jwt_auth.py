from flask_jwt_extended import JWTManager, create_access_token
from models.user import User

jwt = JWTManager()

def init_jwt(app):
    jwt.init_app(app)

def create_token(user):
    return create_access_token(identity=user)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id  # Retorna o UUID como string

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]  # Pega o UUID do token
    return User.find_by_id(identity)  # Busca usuário pelo UUID


