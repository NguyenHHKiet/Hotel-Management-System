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
    a_type = db.Column(db.String(length=30), nullable=False)
    a_status = db.Column(db.String(length=30), nullable=False)
    a_capacity = db.Column(db.String(length=30), nullable=False)
    a_title = db.Column(db.String(length=30), nullable=False, unique=True)
    a_description = db.Column(db.String(length=200), nullable=False)

    

class Room(db.Model):
    __tablename__= "rooms"
    r_id = db.Column(db.Integer(), primary_key=True)
    type_id = db.Column(db.Integer(), nullable=False)
    r_number = db.Column(db.String(length=30), nullable=False, unique=True)
    r_price = db.Column(db.String(length=30), nullable=False)
    r_status = db.Column(db.String(length=30), nullable=False)
    r_capacity = db.Column(db.String(length=30), nullable=False)

    

class Booking(db.Model):
    __tablename__= "bookings"
    b_id = db.Column(db.Integer(), primary_key=True)
    b_status = db.Column(db.String(length=30), nullable=False)
    st = db.Column(db.String(length=30), nullable=False)
    et = db.Column(db.String(length=30), nullable=False)

class Guests(db.Model):
    __tablename__= "guests"
    g_id = db.Column(db.Integer(), primary_key=True)
    g_status = db.Column(db.String(length=30), nullable=False)
    g_name = db.Column(db.String(length=30), nullable=False)
    g_count = db.Column(db.String(length=30), nullable=False)
    g_email = db.Column(db.String(length=30), nullable=False, unique=True)
    g_streetno = db.Column(db.String(length=200), nullable=False)
    g_city = db.Column(db.String(length=200), nullable=False)
    g_state = db.Column(db.String(length=30), nullable=False)   
    g_country = db.Column(db.String(length=200), nullable=False)
    g_pincode = db.Column(db.String(length=30), nullable=False, unique=True)

    

class Charges(db.Model):
    __tablename__= "charges"
    code = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Integer(), primary_key=True)
    cost = db.Column(db.Integer(), nullable=False, unique=True)


class Job(db.Model):
    __tablename__= "job"
    job_id = db.Column(db.Integer(), primary_key=True)
    job_title = db.Column(db.String(length=200), nullable=False)
    salary = db.Column(db.Integer(), nullable=False)


class Employee(db.Model):
    __tablename__= "employees"
    emp_id = db.Column(db.Integer(), primary_key=True)
    job_id = db.Column(db.Integer(), nullable=False)
    emp_name = db.Column(db.String(length=30), nullable=False)
    emp_email = db.Column(db.String(length=30), nullable=False, unique=True)
    emp_streetno = db.Column(db.String(length=200), nullable=False)
    emp_city = db.Column(db.String(length=200), nullable=False)
    emp_country = db.Column(db.String(length=200), nullable=False)
    emp_phone = db.Column(db.String(length=200), nullable=False)


class Transaction(db.Model):
    __tablename__= "transactions"
    transaction_id = db.Column(db.Integer(), primary_key=True)
    emp_id = db.Column(db.Integer(), nullable=False)
    job_id = db.Column(db.Integer(), nullable=False)
    res_id = db.Column(db.Integer(), nullable=False)
    dated = db.Column(db.DateTime())
    amount = db.Column(db.String(length=30), nullable=False)
    payment_mode = db.Column(db.String(length=200), nullable=False)
    type = db.Column(db.String(length=200), nullable=False)
    status = db.Column(db.String(length=200), nullable=False)


class Type(db.Model):
    __tablename__= "rooms_type"
    type_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=200), nullable=False)
    capacity = db.Column(db.String(length=30), nullable=False)


class Reservation(db.Model):
    __tablename__= "reservation"
    res_id = db.Column(db.Integer(), primary_key=True)
    g_id = db.Column(db.Integer(), nullable=False)
    r_id = db.Column(db.Integer(), nullable=False)
    transaction_id = db.Column(db.Integer(), nullable=False)
    in_date = db.Column(db.DateTime())
    out_date = db.Column(db.DateTime())
    days = db.Column(db.Integer())
