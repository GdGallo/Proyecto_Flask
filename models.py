from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"

    # Definición de columnas para el modelo User
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)  # Nombre de usuario único
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único
    password = db.Column(db.String(120), nullable=False)  # Contraseña

    # Relación inversa con el modelo Post
    posts = db.relationship("Post", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    __tablename__ = "post"

    # Definición de columnas para el modelo Post
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # Relación con User
    created = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)  # Fecha de creación
    title = db.Column(db.String, nullable=False)  # Título del post
    body = db.Column(db.Text, nullable=False)  # Cuerpo del post

    # Relación con el modelo User
    author = db.relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post {self.id}, {self.title}>"


class ConversationMemory(db.Model):
    __tablename__ = "conversation_memory"

    # Definición de columnas para el modelo ConversationMemory
    id = db.Column(db.Integer, primary_key=True)  # ID único
    session_id = db.Column(db.String(100), nullable=False)  # Identificador de la sesión
    user_input = db.Column(db.Text, nullable=False)  # Entrada del usuario
    bot_response = db.Column(db.Text, nullable=False)  # Respuesta del bot
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Marca de tiempo de la conversación

    def __repr__(self):
        return f"<ConversationMemory {self.id}>"
