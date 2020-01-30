from flask_wtf import FlaskForm
from wtforms import TextField, SelectMultipleField, SubmitField, SelectField
from wtforms.widgets import ListWidget, CheckboxInput

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class create_contractForm(FlaskForm):
    receiver = TextField('Receiver')
    sendFile = SelectField('File', choices=[('1', 'File1'), ('2', 'File2')])
    conditions = MultiCheckboxField('Conditions', choices=[('1', 'Do not share'), ('2', 'Classified'), ('3', 'DND')])
    submit = SubmitField('Create contract')