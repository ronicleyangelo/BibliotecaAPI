# Exporta as funções principais do JWT
from .jwt_auth import jwt, init_jwt, create_token

__all__ = ['jwt', 'init_jwt', 'create_token']