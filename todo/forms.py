from flask_wtf.file import FileAllowed
from todo import bcrypt
from todo.model import User
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class SignupForm(FlaskForm):
    def validate_email(form, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, Please Choose a different email.')

    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Code')


class ResetForm(FlaskForm):
    def vaildCode(form, field):
        user = User.query.filter_by(token=form.code.data).first()
        test = bcrypt.check_password_hash(user.password, form.password.data)
        if not test:
            raise ValidationError("Your code has expired")

    code = StringField('Code', validators=[vaildCode])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = FieldList('Items', validators=[DataRequired()])
    submit = SubmitField('Done')


class UpdateAccountForm(FlaskForm):
    name = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
