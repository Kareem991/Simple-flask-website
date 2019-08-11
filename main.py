from flask import *
from . import db
from .models import User
from flask_login import login_required, current_user, login_user, logout_user
from . import mail
from flask_mail import Message
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from profanity_check import predict

main = Blueprint('main', __name__)


@main.route('/',methods=['GET','POST'])
def index():
	error = None
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		user = User.query.filter_by(email=email).first()
		if len(request.form['password']) <1 :
			error='Invalid password'
		elif len(request.form['email']) <1 :
			error='Invalid email'	
		elif not user:
			error='Such email does not exist'
		elif user.password != password:
			error='Wrong password'	 	
		else:
			login_user(user)
			return redirect(url_for('main.profile'))

	if  current_user.is_authenticated != True :
		return render_template('login.html', error=error)
	else:
		return redirect(url_for('main.profile'))
			
@main.route('/reset_password',methods=['GET','POST'])
def reset_password():
	error=None
	warn=None
	if request.method == 'POST':
		email = request.form.get('email')
		user = User.query.filter_by(email=email).first()
		if not user:
			error='Such email does not exist'
		else:
			msg=Message(subject="Reset password",body='This mail was sent to you because you requested to reset your password',sender='from@example.com',recipients=[email])
			mail.send(msg)
			warn='We have sent you a link to reset your password, check your mail!'
	if  current_user.is_authenticated != True :
		return render_template('reset_password.html',error=error,warn=warn)
	else:
		return redirect(url_for('main.profile'))	

@main.route('/profile',methods=['GET'])
@login_required
def profile():
	return render_template('profile.html',name=current_user.username,email=current_user.email)

@main.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))


@main.route('/upload',methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect(url_for('main.upload'))
	else:
		return render_template('upload.html')		

@main.route('/info')
def info():
	user_agent = request.user_agent
	platform = user_agent.platform
	browser = user_agent.browser
	version = user_agent.version
	
	return render_template('info.html',platform=platform,browser=browser,version=version)

@main.route('/distance')
def distance():
	return "under construction"
@main.route('/mean_filter',methods=['GET','POST'])
def mean_filter():
	output=None
	answer=None
	if request.method=='POST':
		text=request.form['text_provided']
		output=predict([text])
		if(output):
			answer='The text is offensive!'
		else:
			answer='The text is not offensive!'	

		
	return render_template('mean.html',answer=answer)

		
		


