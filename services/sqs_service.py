class SQSService:
    def __init__(self):
        print("SQS Service iniciado")
    
    def send_book_notification(self, user_id, book_title, action):
        message = {
            'user_id': user_id,
            'book_title': book_title,
            'action': action
        }
        print(f"📨 Notificação: {message}")
        return True