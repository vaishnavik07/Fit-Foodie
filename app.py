import os
from flask import Flask
from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image
from ml_model import food_identifier
from food import nutrients

app = Flask(__name__)
mysql = MySQL(app)


app.secret_key = 'xyz623'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vrk17#2002'
app.config['MYSQL_DB'] = 'geeklogin'


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', ( email, password, ))
		cursor.execute('SELECT password FROM accounts WHERE email = % s', ( email, ))
		account = cursor.fetchone()
		print(account)
		if account:
			print("Inside account")
			if account['password'] == password:
				msg = 'Logged in successfully !'
				return render_template('home.html', msg = msg,email=email,account=account)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/home',methods =['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			print(msg)
			return redirect(url_for('login'))
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload',methods=['GET'])
def upload():
    return render_template('uploads.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        image = Image.open(file)
        # Get the current working directory
        cwd = os.path.dirname(os.path.abspath(__file__))

        file_path=os.path.join(cwd,UPLOAD_FOLDER,filename)
        # print(file_path)
        resized_img = image.resize((400, 400))
        resized_img.save(file_path)
        food_name=food_identifier(file_path)
        nutr=nutrients(food_name)
        print(food_name)
        print(nutr)
        # return render_template("result.html", result=food_name)
        return render_template('uploads.html', filename=filename, food=food_name,nutr=nutr)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)