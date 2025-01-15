from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    # Relación inversa de los posts del usuario
    posts = db.relationship('Post', back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)

    # Relación con el modelo User (si tienes un modelo de usuario)
    author = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.id}, {self.title}>'
   

