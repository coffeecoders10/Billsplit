from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_mail = db.Column(db.String(255), unique=True, nullable=False)
    user_username = db.Column(db.String(255), nullable=False)
    # userinfo = db.relationship('UserInfo', backref='user', lazy=True)
    # expenses = db.relationship('Expenses', backref='user', lazy=True)
    # balances_1 = db.relationship('Balances', foreign_keys='Balances.balances_user_id_1', backref='user1', lazy=True)
    # balances_2 = db.relationship('Balances', foreign_keys='Balances.balances_user_id_2', backref='user2', lazy=True)

class UserInfo(db.Model):
    userinfo_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    userinfo_name = db.Column(db.String(255), nullable=False)
    userinfo_dob = db.Column(db.Date)
    userinfo_gender = db.Column(db.String(10))
    userinfo_positive_balance = db.Column(db.Float)
    userinfo_negative_balance = db.Column(db.Float)

class Expenses(db.Model):
    expenses_id = db.Column(db.Integer, primary_key=True)
    expenses_total = db.Column(db.Float)
    expenses_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    expenses_names = db.Column(db.String(255))
    expenses_reason = db.Column(db.String(255))
    expenses_reciept = db.Column(db.String(255))

class Groups(db.Model):
    groups_id = db.Column(db.Integer, primary_key=True)
    groups_name = db.Column(db.String(255), unique=True, nullable=False)
    groups_type = db.Column(db.String(50))

class GroupInfo(db.Model):
    groupinfo_group_id = db.Column(db.Integer, db.ForeignKey('groups.groups_id'), primary_key=True)
    groupinfo_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)

class Transactions(db.Model):
    transactions_payer_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    transactions_payee_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    transactions_group_id = db.Column(db.Integer, db.ForeignKey('groups.groups_id'), primary_key=True)
    transactions_amount = db.Column(db.Float)
    transactions_expenses_id = db.Column(db.Integer, db.ForeignKey('expenses.expenses_id'), primary_key=True)

class Balances(db.Model):
    balances_user_id_1 = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    balances_user_id_2 = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    balances_group_id = db.Column(db.Integer, db.ForeignKey('groups.groups_id'), primary_key=True)
    balances_amount = db.Column(db.Float)

class SimplifiedBalances(db.Model):
    simp_balances_user_id_1 = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    simp_balances_user_id_2 = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    simp_balances_group_id = db.Column(db.Integer, db.ForeignKey('groups.groups_id'), primary_key=True)
    simp_balances_amount = db.Column(db.Float)
