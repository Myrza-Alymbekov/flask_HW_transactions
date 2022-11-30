from flask_wtf import FlaskForm
import wtforms as ws
from app import app
from .models import Status



class TransactionsForm(FlaskForm):
    period = ws.StringField('Период')
    value = ws.IntegerField('Сумма')
    status_id = ws.SelectField('Статус транзакции', choices=[])
    unit = ws.StringField('Валюта')
    subject = ws.StringField('Комментарии')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_choices = []
        with app.app_context():
            for status in Status.query.all():
                self.status_choices.append((status.id, status.name))
        self._fields['status_id'].choices = self.status_choices

    def validate(self):
        if not super().validate():
            return False
        error_counter = 0

        if self.value.data < 0:
            self.value.errors.append('Сумма не может быть отрицательной')
            error_counter += 1

        if error_counter > 0:
            return False
        else:
            return True


class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=4, max=20)
    ])
    password = ws.PasswordField('Пароль', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=8, max=24)
    ])
