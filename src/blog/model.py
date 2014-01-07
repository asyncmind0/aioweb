from aioweb.db.model import Model

class Post(Model):
    required_fields = ['title', 'body', 'date']