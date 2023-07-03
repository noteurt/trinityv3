from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap5
import requests

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ColorInput

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvViaasdffNqIRVWOG'


# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    form = Settigns()
    message = ""
    if form.validate_on_submit():
        message = send_data(form)  # Call the send_data function and store the message
    return render_template('settings.html', form=form, message=message)

def send_data(form):
    try:
        response = requests.post('https://localhost:3000/setSettings', json=form.data)
        
        # Check the response status code
        if response.status_code == 200:
            # If the request was successful, return the response from the external API
            result = response.json()
            return 'Data sent successfully'
        else:
            # If the request was unsuccessful, return an error message
            return 'Failed to send data to the external API'
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return 'Error: ' + str(e)


@app.route("/message", methods=['GET', 'POST'])
def message():
    form = Message()
    message = ""
    if form.validate_on_submit():
        nachricht = form.nachricht.data
        message = nachricht
        return message
    return render_template('message.html', form=form, message=message)

@app.route("/")
def index():
    return render_template('index.html')

class Settigns(FlaskForm):
    ip = StringField('IP Adresse', validators=[DataRequired(), Length(7, 15)])
    port = IntegerField('Port')
    spalten = IntegerField('Spalten')
    zeilen = IntegerField('Zeilen')
    submit = SubmitField('Absenden')

class Message(FlaskForm):
    nachricht = StringField('Nachricht', validators=[DataRequired()])
    #r = IntegerField('R', validators=[DataRequired()])
    annimated = BooleanField('Animited')
    background_color = StringField('Farbe', widget=ColorInput())
    submit = SubmitField('Absenden')