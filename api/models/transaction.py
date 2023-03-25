from extensions.sqlalchemy import database

class Transaction(database.Model):
    __tablename__ = 'transactions'

    transaction_id = database.Column(database.Integer, database.Sequence('transaction_id_seq'), primary_key=True)
    amount = database.Column(database.Float)
    transaction_type = database.Column(database.Enum('deposit', 'transfer', 'withdraw', name='transaction_type'))
    date = database.Column(database.DateTime)
    source_account_id = database.Column(database.Integer, database.ForeignKey('accounts.account_id', ondelete='CASCADE'))
    recipient_account_id = database.Column(database.Integer, database.ForeignKey('accounts.account_id', ondelete='CASCADE'))

    source_account = database.relationship('Account', foreign_keys=[source_account_id], backref='outgoing_transactions', cascade="all, delete", lazy=True)
    recipient_account = database.relationship('Account', foreign_keys=[recipient_account_id], backref='incoming_transactions', cascade="all, delete", lazy=True)