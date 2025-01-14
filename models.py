from extensions import db

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User{self.username}>'