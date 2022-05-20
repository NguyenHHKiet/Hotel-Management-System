from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])

class AmenityForm(FlaskForm):
    id = StringField('ID', validators=[Length(min=0, max=5), DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    capacity = StringField('Capacity', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])


class RoomForm(FlaskForm):
    id = StringField('ID', validators=[Length(min=3, max=5), DataRequired()])
    number = StringField('Room Number', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    capacity = StringField('Capacity', validators=[DataRequired()])

class DateForm(FlaskForm):
    dt = DateField('Pick a Date', format="%m/%d/%Y")

class BillForm(FlaskForm):
    id = StringField('Guest ID', validators=[Length(min=1, max=5), DataRequired()])

class BookingForm(FlaskForm):
    id = StringField('Enter your unique Guest ID')
    check_in = DateField('Pick a Date', format="%m/%d/%Y")
    check_out = DateField('Pick a Date', format="%m/%d/%Y")
    status = StringField('Status')
    name = StringField('Name', validators=[DataRequired()])
    count = StringField('No of adults', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    streetno = TextAreaField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])    
    country = StringField('Country', validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired()])
