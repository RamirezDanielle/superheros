from flask import Flask, request, render_template, redirect, session
import os 
import requests
# import pprint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_superhero', methods=['POST'])
def get_superhero():
    search = request.form['search']
    print(search)
    headers = os.environ.get("KEY")
    url = f"https://superheroapi.com/api/{headers}/search/{search}"
    print(url)
    response = requests.get(url)
    print(response.json())
   
 
    return('/')


if __name__=='__main__':
    app.run(debug=True)