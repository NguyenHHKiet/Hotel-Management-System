from flask_wtf import Form
from wtforms import DateField, StringField, TextAreaField, PasswordField, validators

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=150),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

class AmenityForm(Form):
    id = StringField('ID', [validators.Length(min=0, max=5)])
    type = StringField('Type', [validators.Length(min=0, max=1)])
    status = StringField('Status', [validators.Length(min=0, max=1)])
    capacity = StringField('Capacity', [validators.Length(min=0, max=5)])
    title = StringField('Title', [validators.Length(min=2, max=200)])
    description = TextAreaField('Description', [validators.Length(min=30)])

class RoomForm(Form):
    id = StringField('ID', [validators.Length(min=3, max=5)])
    number = StringField('Room Number', [validators.Length(min=1, max=3)])
    type = StringField('Type', [validators.Length(min=1, max=1)])
    status = StringField('Status', [validators.Length(min=1, max=1)])
    capacity = StringField('Capacity', [validators.Length(min=1, max=2)])

class DateForm(Form):
    dt = DateField('Pick a Date', format="%m/%d/%Y")

class BookingForm(Form):
    g_id = StringField('Enter your unique Guest ID')
    check_in = DateField('Pick a Date', format="%m/%d/%Y")
    check_out = DateField('Pick a Date', format="%m/%d/%Y")
    status = StringField('Status')
    name = StringField('Name', [validators.Length(min=3, max=30)])
    count = StringField('No of adults', [validators.Length(min=1, max=1)])
    email = StringField('Email', [validators.Length(min=2, max=200)])
    streetno = TextAreaField('Street Address', [validators.Length(min=6)])
    city = StringField('City', [validators.Length(min=2, max=200)])
    state = StringField('State', [validators.Length(min=2, max=200)])    
    country = StringField('Country', [validators.Length(min=2, max=20)])
    pincode = StringField('Pincode', [validators.Length(min=6, max=6)])

class BillForm(Form):
    id = StringField('Guest ID', [validators.Length(min=1, max=5)])

