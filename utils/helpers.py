def validate_book_data(data):
    if not data.get('title') or not data.get('author'):
        return False, "Título e autor são obrigatórios"
    return True, ""

def format_response(success, message, data=None, status_code=200):
    return {
        'success': success,
        'message': message,
        'data': data
    }, status_code