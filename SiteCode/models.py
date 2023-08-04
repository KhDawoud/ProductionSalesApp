from SiteCode import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return SalesPerson.query.get(int(user_id))


class SalesPerson(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    entity = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    progresses = db.relationship('Progress', backref='salesperson', lazy=True)
    companies_available = db.Column(db.String(80), nullable=True)
    daily_messages = db.relationship('DailyMessage', back_populates='salesperson', lazy=True)
    content_messages = db.relationship('ContentMessage', back_populates='salesperson', lazy=True)
    lead = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return f"<SalesPerson(id={self.id}, username='{self.username}', email='{self.email}', entity='{self.entity}')>"


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(40), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    country = db.Column(db.String(60), nullable=False)
    communication = db.Column(db.String(15), nullable=False)
    bpo = db.Column(db.String(50), nullable=False)
    name_call = db.Column(db.String(30), nullable=False)
    conversation = db.Column(db.String(50), nullable=False)
    response = db.Column(db.Text, nullable=True)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('sales_person.id'), nullable=False)

    def __repr__(self):
        return f"<Progress(id={self.id}, company_name='{self.company_name}', date='{self.date}'," \
               f" country='{self.country}', name_call='{self.name_call}')>"


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    skype = db.Column(db.String(120), nullable=False, unique=True)
    relation = db.Column(db.String(30), nullable=False)
    destinations = db.Column(db.Text, nullable=False)
    entity = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Partner(name='{self.name}', email='{self.email}', skype='{self.skype}'," \
               f" relation='{self.relation}', destinations='{self.destinations}')"


class DailyMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('sales_person.id'), nullable=False)
    salesperson = db.relationship('SalesPerson', back_populates='daily_messages')

    def __repr__(self):
        return f"<DailyMessage(id={self.id}, date='{self.date}', message='{self.message}')>"


class ContentMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('sales_person.id'), nullable=False)
    salesperson = db.relationship('SalesPerson', back_populates='content_messages')

    def __repr__(self):
        return f"<ContentMessage(id={self.id}, date='{self.date}', message='{self.message}')>"
