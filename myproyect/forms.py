from wtforms import ValidationError, PasswordField, EmailField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Email, EqualTo, DataRequired, Length
from myproyect.models import Users

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[EqualTo('password_confirm', 'Passwords must match'), DataRequired(), Length(min=5, max=25)])
    password_confirm = PasswordField('Confirm your password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use, try logging in')
        

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=25)])
    submit = SubmitField('Log In')

    def validate_email(self, field):
        if not Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email not yet registered, try registering')
    
    def validate_password(self, field):
        user = Users.query.filter_by(email=self.email.data).first()
        if user:
            if not user.check_password(field.data):
                raise ValidationError('Incorrect Password')
        

class LoginGoogleForm(FlaskForm):
    submit = SubmitField('Log In with Google')
    