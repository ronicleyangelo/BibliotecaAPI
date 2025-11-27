from models.book import Book

class LambdaService:
    def __init__(self):
        print("Lambda Service iniciado")
    
    def get_user_statistics(self, user_id):
        books = Book.find_by_user(user_id)
        total_books = len(books)
        read_books = len([b for b in books if b.status == 'lido'])
        
        return {
            'total_books': total_books,
            'read_books': read_books,
            'to_read_books': total_books - read_books,
            'completion_rate': (read_books / total_books * 100) if total_books > 0 else 0
        }