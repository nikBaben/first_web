from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,IntegerField
from wtforms.validators import DataRequired,  Email, Length, EqualTo,Optional
from wtforms.widgets import TextArea, TextInput, PasswordInput, CheckboxInput

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Видимое имя на сайте', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()], widget=PasswordInput())
    password_confirmation = StringField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')], widget=PasswordInput())

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Пароль', validators=[DataRequired()], widget=PasswordInput())
    remember_me = BooleanField('Запомнить меня', widget=CheckboxInput())


class ArticleForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    body = StringField('Описание', validators=[DataRequired()], widget=TextArea())
    price = StringField('Примерная стоимость', validators=[DataRequired()], widget=TextArea())
    address = StringField('адрес', validators=[DataRequired()])
    img = StringField('Картинка(ссылка)', validators=[DataRequired()])
    category_id = IntegerField('ID категории', validators=[Optional()], widget=TextInput('number'))

class OtzivForm(FlaskForm):
    about = StringField('Название товара', validators=[DataRequired()])
    lol = StringField('Описание', validators=[DataRequired()], widget=TextArea())
    star = StringField('Название товара', validators=[DataRequired()])
    post_id = IntegerField('ID категории', validators=[Optional()], widget=TextInput('number'))