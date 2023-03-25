from extensions.sqlalchemy import database


class Account(database.Model):
    __tablename__ = 'accounts'

    account_id = database.Column(database.Integer, database.Sequence('account_id_seq'), primary_key=True)
    account_type = database.Column(database.Enum('savings', 'checking', name='type'))
    balance = database.Column(database.Float, default=0)
    user_id = database.Column(database.Integer, database.ForeignKey('users.user_id', ondelete='CASCADE'))
    account_number = database.Column(database.String(10))
    created_at = database.Column(database.DateTime)
    modified_at = database.Column(database.DateTime)
    active = database.Column(database.Boolean, default=True, nullable=False)
    
    #transaction = database.relationship('Transaction',  backref='accounts', cascade="all, delete", lazy=True)