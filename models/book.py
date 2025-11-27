from tinydb import TinyDB, Query
import uuid
from datetime import datetime

db = TinyDB('database/db.json')
books_table = db.table('books')
BookQuery = Query()

class Book:
    def __init__(self, title, author, user_id, status="para_ler", **kwargs):
        self.id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.user_id = user_id
        self.status = status
        self.genre = kwargs.get('genre')
        self.pages = kwargs.get('pages')
        self.rating = kwargs.get('rating')
        self.created_at = datetime.utcnow().isoformat()
    
    def save(self):
        books_table.insert(self.to_dict())
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        books_table.update(self.to_dict(), BookQuery.id == self.id)
    
    def delete(self):
        books_table.remove(BookQuery.id == self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'user_id': self.user_id,
            'status': self.status,
            'genre': self.genre,
            'pages': self.pages,
            'rating': self.rating,
            'created_at': self.created_at
        }
    
    @classmethod
    def find_by_id(cls, book_id):
        book_data = books_table.get(BookQuery.id == book_id)
        if book_data:
            return cls.from_dict(book_data)
        return None
    
    @classmethod
    def find_by_user(cls, user_id, status=None):
        query = BookQuery.user_id == user_id
        if status:
            query = query & (BookQuery.status == status)
        
        books_data = books_table.search(query)
        return [cls.from_dict(book_data) for book_data in books_data]
    
    @classmethod
    def search_books(cls, user_id, search_term):
        books_data = books_table.search(
            (BookQuery.user_id == user_id) & 
            ((BookQuery.title.matches(f'.*{search_term}.*')) | 
             (BookQuery.author.matches(f'.*{search_term}.*')))
        )
        return [cls.from_dict(book_data) for book_data in books_data]
    
    @classmethod
    def from_dict(cls, data):
        book = cls(
            title=data['title'],
            author=data['author'],
            user_id=data['user_id'],
            status=data.get('status', 'para_ler')
        )
        book.id = data['id']
        book.genre = data.get('genre')
        book.pages = data.get('pages')
        book.rating = data.get('rating')
        book.created_at = data.get('created_at')
        return book