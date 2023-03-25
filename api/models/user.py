from extensions.sqlalchemy import database
from werkzeug.security import check_password_hash, generate_password_hash

class User(database.Model):
    __tablename__ = 'users'

    user_id = database.Column(database.Integer, database.Sequence('users_id_seq'), primary_key=True)
    username = database.Column(database.String(80))
    email = database.Column(database.String(80))
    password = database.Column(database.String(100))
    created_at = database.Column(database.DateTime)
    modified_at = database.Column(database.DateTime)
    active = database.Column(database.Boolean, default=True, nullable=False)

    account = database.relationship('Account',  backref='users', cascade="all, delete", lazy=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def check_user_satus(self):
        return self.active
    
    def generate_password(self, password):
        return generate_password_hash(password, method='sha256')