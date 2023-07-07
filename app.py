from flask import Flask, render_template, redirect, url_for, jsonify, request, current_app
from flask_bootstrap import Bootstrap5
import requests
import json

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
    settings_from_backend = get_settings()
    if form.validate_on_submit():
        message = send_data(form, "setSettings")  # Call the send_data function and store the message
    elif (not(type(settings_from_backend) == str)):
        form.ip.data = settings_from_backend.ip
        form.port.data = settings_from_backend.port
        form.width.data = settings_from_backend.width
        form.height.data = settings_from_backend.height
    else:
        message = settings_from_backend

    return render_template('settings.html', form=form, message=message)

@app.route("/message", methods=['GET', 'POST'])
def message():
    form = Message()
    message = ""
    if form.validate_on_submit():
        message = send_data(form, "setMessage")  # Call the send_data function and store the message
    return render_template('message.html', form=form, message=message)

@app.route("/color", methods=['GET', 'POST'])
def color():
    form = Color()
    message = ""
    if form.validate_on_submit():
        message = send_data(form, "setMessage")  # Call the send_data function and store the message
    return render_template('color.html', form=form, message=message)

@app.route("/sensor", methods=['GET', 'POST'])
def sensor():
    message = ""
    rooms = get_sensor()
    current_app.logger.info(rooms)
    return render_template('sensor.html', rooms=rooms, message=message)

@app.route("/")
def index():
    return render_template('index.html')



 ### Formulare   

class Settigns(FlaskForm):
    ip = StringField('IP Adresse', validators=[DataRequired(), Length(7, 15)])
    port = IntegerField('Port')
    width = IntegerField('Spalten')
    height = IntegerField('Zeilen')
    submit = SubmitField('Absenden')

class Message(FlaskForm):
    message = StringField('Nachricht', validators=[DataRequired()])
    #r = IntegerField('R', validators=[DataRequired()])
    animation = BooleanField('Animited')
    background_color = StringField('Farbe', widget=ColorInput())
    submit = SubmitField('Absenden')

class Color(FlaskForm):
    #message = StringField('Nachricht', validators=[DataRequired()])
    #r = IntegerField('R', validators=[DataRequired()])
    #annimated = BooleanField('Animited')
    background_color = StringField('Farbe', widget=ColorInput())
    submit = SubmitField('Absenden')

###Sende Methode zum Backend

def send_data(form, endpoint):
    try:
        response = requests.post('https://localhost:8080/' + endpoint, json=form.data)
        
        # Check the response status code
        if response.status_code == 200:
            # If the request was successful, return the response from the external API
            result = response.json()
            return 'Anfrage erflogreich gesendet'
        else:
            # If the request was unsuccessful, return an error message
            return 'Fehler beim senden'
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return 'Error: ' + str(e)

### Get Methode zum Backend
def get_settings():
    try:
        response = requests.get('https://localhost:8080/getSettings')
        
        # Check the response status code
        if response.status_code == 200:
            # If the request was successful, return the response from the external API
            result = response.json()
            return result
        else:
            # If the request was unsuccessful, return an error message
            return 'Fehler beim senden'
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return 'Error: ' + str(e)

def get_sensor():
    try:
        # change URL in production
        response = requests.get('http://localhost:5000/api/mockdata/sensor')
        
        # Check the response status code
        if response.status_code == 200:
            # If the request was successful, return the response from the external API
            result = response.json()
            return result
        else:
            # If the request was unsuccessful, return an error message
            return 'Fehler beim senden'
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return 'Error: ' + str(e)


# just for development
@app.route('/api/mockdata/sensor', methods=['GET'])
def get_mock_data():
    # Create your mock data as a Python dictionary or list
    mock_data = [
        {
        'room': 'A111',
        'temperature': 30,
        'mac': '10:20:30:40:50:60'
        },
        {
        'room': 'A211',
        'temperature': 40,
        'mac': '10:20:30:40:50:60'
        },
        {
        'room': 'A311',
        'temperature': 50,
        'mac': '10:20:30:40:50:60'
        },
        {
        'room': 'A411',
        'temperature': 50,
        'mac': '10:20:30:40:50:60'
        }
    ]

    # Convert the mock data to JSON format
    #json_data = json.dumps(mock_data)

    # Return the JSON response
    return jsonify(mock_data)
