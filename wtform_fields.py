from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import User

def invalid_credentials(form, field):
    """ Verificador de usuario y contraseña """

    username_entered = form.username.data
    password_entered = field.data

    #Verificar que el nombre de usuario existe
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("EL nickname o la constraseña son incorrectos.")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("El nickname o la contraseña son incorrectos.")


    
class RegistrationForm(FlaskForm):
    """ Página de registro """

    username = StringField('username_label', 
    validators=[InputRequired(message="Username required"), 
    Length(min=4, max=25, message="El nombre de usuario debe de tener entre 4 y 25 caracteres.")])


    password = PasswordField('password-label', 
    validators=[InputRequired(message="Contraseña requerida."), 
    Length(min=4, max=25, message="La contraseña debe de tener entre 4 y 25 caracteres.")])


    confirm_pswd = PasswordField('confirm_pswd_label', 
    validators=[InputRequired(message="Contraseña requerida."), 
    EqualTo('password', message="Las contraseñas deben coincidir." )
    ])


    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Ese nickname ya existe, esoge otro.")


class LoginForm(FlaskForm):
    """ Formulario de logeo. """

    username = StringField('username_label', validators=[InputRequired(message="El nickname es requerido.")])
    password = PasswordField('password_label', validators=[InputRequired(message="La contraseña es requerida."), invalid_credentials])
    submit_button = SubmitField('Iniciar sesión')
