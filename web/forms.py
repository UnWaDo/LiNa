from wtforms import StringField, PasswordField, SubmitField, SelectField
from flask_wtf import Form
from wtforms.validators import DataRequired


class LoginForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('pass', validators=[DataRequired()])


class Level1Form(Form):
    submit = SubmitField('Начать игру')


class Level2Form(Form):
    ch = [('п', 'п'), ('о', 'о'), ('ж', 'ж'), ('а', 'а')]
    let1 = SelectField('1', choices=ch)
    let2 = SelectField('2', choices=ch)
    let3 = SelectField('3', choices=ch)
    let4 = SelectField('4', choices=ch)
    let5 = SelectField('5', choices=ch)
    let6 = SelectField('6', choices=ch)
    let7 = SelectField('7', choices=ch)


class Level3Form(Form):
    ch = []
    for i in range(6):
        ch.append((str(i+1), str(i+1)))
    pic1 = SelectField('1', choices=ch)
    pic2 = SelectField('1', choices=ch)
    pic3 = SelectField('1', choices=ch)
    pic4 = SelectField('1', choices=ch)
    pic5 = SelectField('1', choices=ch)
    pic6 = SelectField('1', choices=ch)


class Level4Form(Form):
    answer = StringField(validators=[DataRequired()])
