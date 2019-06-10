from flask import Flask, jsonify, request
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, abort, app, g, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, IntegerField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, AnyOf, DataRequired, Regexp
from flask_wtf.csrf import CSRFProtect
from werkzeug.datastructures import MultiDict
import os, socket
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import datetime, time
from flask_prometheus import monitor

app = Flask(__name__)
app.secret_key = 'secret'

class OpenTicketForm(FlaskForm):
	your_first_and_second_name = StringField('Please enter your First and Second Name', validators=[InputRequired()])
	your_username = StringField('Your Username', validators=[InputRequired()])
	your_mail_address = StringField('Your Mail Address', validators=[InputRequired()])
	start_date_download = StringField('Start Date of the download', validators=[InputRequired()])
	end_date_download = StringField('End Date of the download', validators=[InputRequired()])
	db_instance = StringField('DataBase Instance', validators=[InputRequired()])

class GetDataForm(FlaskForm):
    db_instance = StringField('db_instance', validators=[InputRequired()])
    start_date_download = StringField('start_date_download', validators=[InputRequired()])
    end_date_download = StringField('end_date_download', validators=[InputRequired()])
    your_mail_address = StringField('your_mail_address', validators=[InputRequired()])

# @app.route("/")
# def index():
# 	return redirect(url_for('home'))

@app.route('/')
def index():
  return "Flask is up & running\n"

@app.route('/success', methods=["GET", "POST"])
def success():
	db_instance = request.args.get('db_instance')
	start_date_download = request.args.get('start_date_download')
	end_date_download = request.args.get('end_date_download')
	your_mail_address = request.args.get('your_mail_address')
	return render_template('get_download_data.html', db_instance = db_instance, start_date_download = start_date_download, end_date_download = end_date_download, your_mail_address=your_mail_address)

@app.route("/home", methods=["GET", "POST"])
def home():
	openticketform = OpenTicketForm()
	if request.method == 'POST': 
		print(request.form)
		db_instance = request.form['db_instance']
		print (type(db_instance))
		start_date_download = request.form['start_date_download']
		end_date_download = request.form['end_date_download']
		your_mail_address = request.form['your_mail_address']
		return redirect(url_for('success',db_instance = db_instance, start_date_download = start_date_download, end_date_download = end_date_download, your_mail_address = your_mail_address))
	return render_template('index.html', openticketform=openticketform)


from os import path
extra_dirs = ['templates','static']
extra_files = extra_dirs[:]
print(extra_files)
for extra_dir in extra_dirs:
	for dirname, dirs, files in os.walk(extra_dir):
		for filename in files:
			filename = path.join(dirname, filename)
			if path.isfile(filename):
				extra_files.append(filename)

# monitoring
monitor(app, port=8000)

app.testing = True

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False, threaded=True, port=5100, extra_files=extra_files)
	#app.run(host='0.0.0.0', debug=False, port=5100,extra_files=extra_files, threaded=True)