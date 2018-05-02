from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class getPreferences(FlaskForm):
    twittername = StringField('twitterhandle', validators=[DataRequired()])
    submit = SubmitField('Show me my preferences')
