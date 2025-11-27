# 📚 Biblioteca Pessoal - API Documentation

## 🚀 Visão Geral
A Biblioteca Pessoal API é uma aplicação Flask para gerenciamento de livros pessoais com autenticação JWT, banco de dados TinyDB e integração com serviços AWS.

---

## 🔐 Rotas de Autenticação

### 1. Registrar Usuário
**URL:** `POST /api/auth/register`

**Autenticação:** Não requer

**Body:**
```json
{
  "username": "string (obrigatório)",
  "password": "string (obrigatório)", 
  "email": "string (opcional)"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Usuário criado",
  "data": {
    "user_id": "uuid"
  }
}
```

### 2. Login
**URL:** `POST /api/auth/login`

**Autenticação:** Não requer

**Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Login realizado",
  "data": {
    "token": "jwt_token"
  }
}
```

---

## 📖 Rotas de Livros (Requerem Autenticação)

### 3. Adicionar Livro
**URL:** `POST /api/books`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "title": "string (obrigatório)",
  "author": "string (obrigatório)",
  "status": "string (para_ler/lendo/lido)",
  "genre": "string",
  "pages": "number",
  "rating": "number"
}
```

### 4. Listar Livros
**URL:** `GET /api/books`

**Query Params:** `?status=para_ler` (opcional)

**Headers:** `Authorization: Bearer <token>`

### 5. Atualizar Livro
**URL:** `PUT /api/books/<book_id>`

**Headers:** `Authorization: Bearer <token>`

**Body:** (campos opcionais para atualização)
```json
{
  "title": "string",
  "author": "string", 
  "status": "string",
  "genre": "string",
  "pages": "number",
  "rating": "number"
}
```

### 6. Deletar Livro
**URL:** `DELETE /api/books/<book_id>`

**Headers:** `Authorization: Bearer <token>`

### 7. Buscar Livros
**URL:** `GET /api/books/search`

**Query Params:** `?q=termo_de_busca`

**Headers:** `Authorization: Bearer <token>`

---

## 📊 Rotas de Estatísticas

### 8. Estatísticas do Usuário
**URL:** `GET /api/statistics`

**Headers:** `Authorization: Bearer <token>`

**Resposta:**
```json
{
  "success": true,
  "message": "Estatísticas",
  "data": {
    "total_livros": 10,
    "lidos": 5,
    "lendo": 2,
    "para_ler": 3
  }
}
```

---

## 🛠 Rotas de Debug (Desenvolvimento)

### 9. Listar Todos os Usuários
**URL:** `GET /api/debug/users`

**Autenticação:** Não requer

### 10. Buscar Usuário por Username
**URL:** `GET /api/debug/find-user/<username>`

**Autenticação:** Não requer

### 11. Health Check
**URL:** `GET /api/health`

**Autenticação:** Não requer

**Resposta:**
```json
{
  "success": true,
  "message": "API online",
  "data": null
}
```

---

## 🔧 Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip

### 1. Configuração do Ambiente
```bash
# Criar estrutura de pastas
mkdir -p biblioteca_pessoal/{database,models,auth,services,utils,aws_lambda}

# Criar arquivos __init__.py
touch biblioteca_pessoal/database/__init__.py
touch biblioteca_pessoal/models/__init__.py
touch biblioteca_pessoal/auth/__init__.py
touch biblioteca_pessoal/services/__init__.py
touch biblioteca_pessoal/utils/__init__.py
touch biblioteca_pessoal/aws_lambda/__init__.py
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar Aplicação
```bash
python app.py
```

**Servidor disponível em:** `http://localhost:5000`

---

## 🧪 Testando a API

### Fluxo Completo de Uso:

```bash
# 1. Registrar usuário
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "senha123", "email": "usuario@email.com"}'

# 2. Fazer login (copiar o token)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "senha123"}'

# 3. Adicionar livro (usar token obtido no login)
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -d '{"title": "Dom Casmurro", "author": "Machado de Assis", "status": "lido"}'

# 4. Listar livros
curl -X GET http://localhost:5000/api/books \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

### Exemplos de Uso com Status:

```bash
# Listar apenas livros "para ler"
curl -X GET "http://localhost:5000/api/books?status=para_ler" \
  -H "Authorization: Bearer SEU_TOKEN_JWT"

# Buscar livros por termo
curl -X GET "http://localhost:5000/api/books/search?q=machado" \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```