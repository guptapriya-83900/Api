# from cmath import log
from lib2to3.pgen2 import token
from flask import Flask,  request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS #pip install -U flask-cors
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    JWTManager,get_jwt_identity,jwt_required
)

import psycopg2 #pip install psycopg2 
import psycopg2.extras
 
app = Flask(__name__)
jwt = JWTManager(app)
  
app.config['SECRET_KEY'] = 'Priya188'
  
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
CORS(app) 
 
DB_HOST = "localhost"
DB_NAME = "userdetails"
DB_USER = "postgres"
DB_PASS = "priya83900"
     
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)  
 
@app.route('/')
def home():
    passhash = generate_password_hash('gopi83900')
    print(passhash)
    return passhash
    
    

@app.route('/login', methods=['POST'])
def login():
    _json = request.json
    user_name = _json['username']
    pass_word = _json['password']
    print(pass_word)
    # validate the received values
    if user_name and pass_word:
        #check user exists          
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
          
        sql = "SELECT * FROM logindetails WHERE username=%s"
        sql_where = (user_name,)
          
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()

        if row  != None and row:
            username = row['username']
            password = row['password']
            if password == pass_word:
                session['username'] = username
                cursor.close()
                access_token = create_access_token(identity=[username,password])
                refresh_token = create_refresh_token([username,password])
                return jsonify({'message' : 'Logged In Successfully!!'},{'access_token': access_token,'refresh_token': refresh_token})
            else:
                resp = jsonify({'message' : 'Bad Request - Invalid password'})
                resp.status_code = 400
                return resp
        else:
            resp = jsonify({'message' : 'Bad Request - Username not available'})
            resp.status_code = 400
            return resp
    else:
        resp = jsonify({'message' : 'Bad Request - Invalid Credentials'})
        resp.status_code = 400
        return resp
          
@app.route('/get_items', methods = ['GET'])
@jwt_required()
def get_items():
    current_user = get_jwt_identity()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM logindetails WHERE username=%s and password =%s"
    sql_where = (current_user[0],current_user[1])
    cursor.execute(sql, sql_where)
    row = cursor.fetchone()
    if row  != None and row:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM item')
        data = cur.fetchall()
        cur.close()
        return  jsonify(data)
    else:
        resp = jsonify({'message' : 'Bad Request - Invalid User'})
        resp.status_code = 400
        return resp    
    
if __name__ == "__main__":
    app.run()