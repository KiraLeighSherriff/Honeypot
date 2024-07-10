from flask import Flask, render_template, request
from waitress import serve

from Database.InsertData import InsertData
from .http_log import HTTPInsert
from .http_alert import HTTPAlert

app = Flask(__name__)
app.secret_key = 'secret'

insert = InsertData()
http_insert = HTTPInsert()
alert = HTTPAlert()
    
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      
        username = request.form['username']
        password = request.form['password']  
        address = request.remote_addr 
       
        alert.AccessAttempt(address, username, password) 
        http_insert.HTTPLogin(address, username, password)
        insert.OtherPorts(address, 80)

    return render_template('attacker_login.html')

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=80)