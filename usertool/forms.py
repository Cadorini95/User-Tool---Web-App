from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class UpdatePlantCostForm(FlaskForm):
    file = FileField('Realizar upload de arquivo .csv ou .xlsx com custos de plantas', validators=[DataRequired()] )
    submit = SubmitField('Confirmar envio do arquivo')

class UpdateMaintCalendarForm(FlaskForm):
    file = FileField('Realizar upload de arquivo .csv ou .xlsx com planos de manutenção programadas', validators=[DataRequired()])
    submit = SubmitField('Confirmar envio do arquivo')
