from flask import Flask, request
from config import Config
from auth.jwt_auth import init_jwt, create_token
from models.user import User
from models.book import Book
from services.sqs_service import SQSService
from services.lambda_service import LambdaService
from utils.helpers import validate_book_data, format_response
from flask_jwt_extended import jwt_required, current_user
import os

app = Flask(__name__)
app.config.from_object(Config)

init_jwt(app)
sqs_service = SQSService()
lambda_service = LambdaService()

os.makedirs('database', exist_ok=True)

# Rotas de Autenticação
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return format_response(False, "Username e password são obrigatórios", None, 400)
    
    if User.find_by_username(data['username']):
        return format_response(False, "Usuário já existe", None, 400)
    
    user = User(
        username=data['username'],
        email=data.get('email'),
        password=data['password']
    )
    user.save()
    
    return format_response(True, "Usuário criado", {'user_id': user.id}, 201)
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    print("=== DEBUG LOGIN ===")
    print("Dados recebidos:", data)
    
    username = data.get('username')
    password = data.get('password')
    
    user = User.find_by_username(username)
    print("Usuário encontrado:", user is not None)
    
    if user:
        print("ID do usuário:", user.id)
        print("Username:", user.username)
        print("Tem password_hash:", bool(user.password_hash))
        print("Hash armazenado:", user.password_hash)
        
        # Testar a senha
        password_match = user.check_password(password)
        print("Senha confere:", password_match)
        
        if not password_match:
            # Tentar algumas senhas comuns para debug
            test_passwords = ['123456', 'password', 'roni', 'admin', '']
            for test_pwd in test_passwords:
                if user.check_password(test_pwd):
                    print(f"⚠️  SENHA ENCONTRADA: '{test_pwd}'")
                    break
    else:
        print("❌ Usuário não encontrado")
    
    print("===================")
    
    if not user or not user.check_password(password):
        return format_response(False, "Credenciais inválidas", None, 401)
    
    token = create_token(user)
    return format_response(True, "Login realizado", {'token': token}, 200)
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     print(data.get('username'), "usuario get")
#     user = User.find_by_username(data.get('username'))
#     if not user or not user.check_password(data.get('password')):
#         return format_response(False, "Credenciais inválidas", None, 401)
    
#     token = create_token(user)
#     return format_response(True, "Login realizado", {'token': token}, 200)

@app.route('/api/debug/users', methods=['GET'])
def debug_users():
    """Rota para debug - listar todos os usuários"""
    all_users = User.get_all_users()
    users_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in all_users]
    
    return format_response(True, f"Total de usuários: {len(users_data)}", users_data, 200)

@app.route('/api/debug/find-user/<username>', methods=['GET'])
def debug_find_user(username):
    """Rota para debug - buscar usuário específico"""
    user = User.find_by_username(username)
    if user:
        return format_response(True, "Usuário encontrado", {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, 200)
    else:
        return format_response(False, "Usuário não encontrado", None, 404)

# Rotas de Livros
@app.route('/api/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    
    is_valid, message = validate_book_data(data)
    if not is_valid:
        return format_response(False, message, None, 400)
    
    book = Book(
        title=data['title'],
        author=data['author'],
        user_id=current_user.id,
        status=data.get('status', 'para_ler'),
        genre=data.get('genre'),
        pages=data.get('pages'),
        rating=data.get('rating')
    )
    book.save()
    
    sqs_service.send_book_notification(current_user.id, book.title, 'adicionado')
    
    return format_response(True, "Livro adicionado", book.to_dict(), 201)

@app.route('/api/books', methods=['GET'])
@jwt_required()
def get_books():
    status = request.args.get('status')
    
    books = Book.find_by_user(current_user.id, status)
    books_data = [book.to_dict() for book in books]
    
    return format_response(True, "Livros listados", books_data, 200)

@app.route('/api/books/<book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    book = Book.find_by_id(book_id)
    
    if not book or book.user_id != current_user.id:
        return format_response(False, "Livro não encontrado", None, 404)
    
    data = request.get_json()
    book.update(**data)
    
    return format_response(True, "Livro atualizado", book.to_dict(), 200)

@app.route('/api/books/<book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    book = Book.find_by_id(book_id)
    
    if not book or book.user_id != current_user.id:
        return format_response(False, "Livro não encontrado", None, 404)
    
    book.delete()
    sqs_service.send_book_notification(current_user.id, book.title, 'removido')
    
    return format_response(True, "Livro removido", None, 200)

@app.route('/api/books/search', methods=['GET'])
@jwt_required()
def search_books():
    search_term = request.args.get('q', '')
    
    books = Book.search_books(current_user.id, search_term)
    books_data = [book.to_dict() for book in books]
    
    return format_response(True, "Busca realizada", books_data, 200)

@app.route('/api/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    statistics = lambda_service.get_user_statistics(current_user.id)
    
    return format_response(True, "Estatísticas", statistics, 200)

@app.route('/api/health', methods=['GET'])
def health_check():
    return format_response(True, "API online", None, 200)

if __name__ == '__main__':
    print("🚀 Biblioteca Pessoal API iniciando...")
    print("📚 http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)