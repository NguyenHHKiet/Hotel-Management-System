from flask import redirect, request, url_for
from hotel import db, login_manager
from hotel import bcrypt
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=100), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f"${self.budget}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

class Amenity(db.Model):
    __tablename__= "amenities"
    a_id = db.Column(db.Integer(), primary_key=True)
    a_type = db.Column(db.String(length=30), nullable=False, unique=True)
    a_status = db.Column(db.String(length=30), nullable=False, unique=True)
    a_capacity = db.Column(db.String(length=30), nullable=False, unique=True)
    a_title = db.Column(db.String(length=30), nullable=False, unique=True)
    a_description = db.Column(db.String(length=200), nullable=False, unique=True)

    

class Room(db.Model):
    __tablename__= "rooms"
    r_id = db.Column(db.Integer(), primary_key=True)
    r_number = db.Column(db.String(length=30), nullable=False, unique=True)
    r_type = db.Column(db.String(length=30), nullable=False, unique=True)
    r_status = db.Column(db.String(length=30), nullable=False, unique=True)
    r_capacity = db.Column(db.String(length=30), nullable=False, unique=True)

    

class Booking(db.Model):
    __tablename__= "bookings"
    b_id = db.Column(db.Integer(), primary_key=True)
    b_status = db.Column(db.String(length=30), nullable=False, unique=True)
    st = db.Column(db.String(length=30), nullable=False, unique=True)
    et = db.Column(db.String(length=30), nullable=False, unique=True)

class Guests(db.Model):
    __tablename__= "guests"
    g_id = db.Column(db.Integer(), primary_key=True)
    g_status = db.Column(db.String(length=30), nullable=False, unique=True)
    g_name = db.Column(db.String(length=30), nullable=False, unique=True)
    g_count = db.Column(db.String(length=30), nullable=False, unique=True)
    g_email = db.Column(db.String(length=30), nullable=False, unique=True)
    g_streetno = db.Column(db.String(length=200), nullable=False, unique=True)
    g_city = db.Column(db.String(length=200), nullable=False, unique=True)
    g_state = db.Column(db.String(length=30), nullable=False, unique=True)   
    g_country = db.Column(db.String(length=200), nullable=False, unique=True)
    g_pincode = db.Column(db.String(length=30), nullable=False, unique=True)

    

class Charges(db.Model):
    __tablename__= "charges"
    code = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Integer(), primary_key=True)
    cost = db.Column(db.Integer(), nullable=False, unique=True)