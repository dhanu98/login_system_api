from flask import Flask, render_template, request, jsonify
import sqlite3,requests

app = Flask(__name__)

@app.route("/formSubmit/", methods=['POST'])
def formSubmit():
    '''formSubmit is method which is used to handle the response from login form
    prepares data required for API and sends request to LoginAPI.
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    j_data = {'email':email,'password':password}
    url= 'http://127.0.0.1:5000/'
    res = requests.post(url,json=j_data)

    '''API Respose Check. If email and password are correct then
    the API returns status code to check and send correct response accordingly. 
    '''
    if res.status_code == 200 :
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/', methods=['GET','POST'])
def login():
    '''Login API to validate Username and password
    This API can be called from submitForm or directly via API Client
    '''
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

   #Database Connection to validate give email and password
        connection = sqlite3.connect("user_data.db")
        cursor = connection.cursor()
        query = "SELECT email, password FROM users WHERE email=? AND password=?"
        cursor.execute(query, (email, password))
        results = cursor.fetchall()

    # Checks if creditials are correct..
        if len(results) > 0:
            return jsonify({'message': 'Login successful'}),200
        else:
            return jsonify({'Invalid email or password'}), 401

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
