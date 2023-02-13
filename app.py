import os 
from flask import Flask 
from flask import Blueprint,render_template,request,redirect,url_for,flash,session 
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


# @app.route('/')
@app.route('/fitFoodie/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', ( email, password, ))
        # cursor.execute('SELECT password FROM accounts WHERE email = % s', ( email, ))
        account = cursor.fetchone()
        print(account)
        if account:
            # Create session data, we can access this data in other route
            session['loggedin'] = True
            session['id'] = account['id']
            # session['email'] = account['email']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        # if account:
        #   print("Inside account")
        #   if account['password'] == password:
        #       msg = 'Logged in successfully !'
        #       return render_template('home.html', msg = msg,email=email,account=account)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/')
def home():
    # Check if user is loggedin
    login=False
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # User is not loggedin redirect to login page
        login=True
        return render_template('home.html', username=session['username'], login=login)
    return render_template('home.html', login=login)
    # return redirect(url_for('home'))

@app.route('/fitFoodie/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/fitFoodie/register', methods =['GET', 'POST'])
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
            # print(msg)
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/fitFoodie/profile')
def profile():
    # Check if user is loggedin
    login=False
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        login=True
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account,login=login)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/fitFoodie/upload',methods=['GET'])
def upload():
    return render_template('uploads.html',login=True)

@app.route('/fitFoodie/upload', methods=['POST'])
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
        # print(nutr)
        nutrients_value=nutr[0]
        print(nutrients_value)
        print(food_name)
        nutr=nutr[1]

        print(nutr)
        print(session['id'])
        print(nutrients_value['fat'])
        print(nutrients_value['carbohydrates'])
        print(nutrients_value['cholesterol'])
        print(nutrients_value['protein'])
        print(nutrients_value['sodium'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO nutrients VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,DEFAULT)', (food_name, session['id'],nutrients_value['fat'],nutrients_value['carbohydrates'],nutrients_value['cholesterol'],nutrients_value['protein'],nutrients_value['sodium'],))
        mysql.connection.commit()
        cursor.close()
        # return render_template("result.html", result=food_name)
        return render_template('uploads.html', filename=filename, food=food_name,nutr=nutr,login=True)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM nutrients WHERE u_id = %s', (session['id'],))
        data=cursor.fetchall()
        cursor.execute('SELECT sum(fat) FROM nutrients WHERE u_id = %s', (session['id'],))
        fat=cursor.fetchall()
        fat=fat[0]['sum(fat)']
        cursor.execute('SELECT sum(carbohydrates) FROM nutrients WHERE u_id = %s', (session['id'],))
        carbohydrates=cursor.fetchall()
        carbohydrates=carbohydrates[0]['sum(carbohydrates)']
        cursor.execute('SELECT sum(cholesterol) FROM nutrients WHERE u_id = %s', (session['id'],))
        cholesterol=cursor.fetchall()
        cholesterol=cholesterol[0]['sum(cholesterol)']
        cursor.execute('SELECT sum(protein) FROM nutrients WHERE u_id = %s', (session['id'],))
        protein=cursor.fetchall()
        protein=protein[0]['sum(protein)']
        cursor.execute('SELECT sum(sodium) FROM nutrients WHERE u_id = %s', (session['id'],))
        sodium=cursor.fetchall()
        sodium=sodium[0]['sum(sodium)']
        cursor.close()
        print(fat)
        # print("data",data[0]['fname'])
        # return redirect(url_for('getAllHistory',data=data))

        return render_template('dashboard.html',data=data,login=True,fat=fat,carbohydrates=carbohydrates,cholesterol=cholesterol,protein=protein,sodium=sodium)
    return render_template('dashboard.html')

    # return render_template('dashboard.html')

@app.route('/getAllHistory')
def getAllHistory():
    if 'loggedin' in session:
        print("hello")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM nutrients WHERE u_id = %s', (session['id'],))
        data=cursor.fetchall()
        cursor.close()
        # print("data",data[0]['fname'])
        return render_template('dashboard.html',data=data)
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
