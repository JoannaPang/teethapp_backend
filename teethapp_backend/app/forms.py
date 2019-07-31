from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    name = StringField('name', validators = [Required()])
#   DataRequired 验证器只是简单地检查相应域提交的数据是否是空
    psw = PasswordField('psw', validators = [Required()])
    email = StringField('email', validators = [Required()])
    submit = SubmitField('Login')
#    remember_me = BooleanField('remember_me', default = False)

class SignupForm(FlaskForm):
    name = StringField('name', validators = [Required()])
    email = StringField('email', validators = [Required()])
    psw = PasswordField('psw', validators = [Required()])
    submit = SubmitField('Signup')

class PhotoForm(FlaskForm):
    username = StringField('username', validators = [Required()])
#    email = StringField('email', validators = [Required()])
    submit = SubmitField('Upload')