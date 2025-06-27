
# for my project i used flask which is used for web development
# for render_template helps me render html pages from the templates.html folder
# while request helps me access the data sent by the user
from flask import Flask, render_template, request, redirect, url_for, session
import os

# __name__ helps me know where to look for my templates folder
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Temporary hardcoded users (in real apps, use a database)
users = {
    "jane": "password123",
    "john": "securepass"
}
# this is the main route that handles the login functionality
# it checks if the user is logged in and redirects them to the welcome page
# if the user is not logged in, it renders the login page
# if the user enters the correct username and password, it redirects them to the welcome page
# if the user enters incorrect credentials, it shows an error message

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            error = "Invalid username or password."
    return render_template('login.html', error=error)

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html', username=session['username'])
 # this is the main function that runs the app, also helps reload my app as well as save changes
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/start', methods=['GET', 'POST'])
def start():
    if 'username' not in session:
        return redirect(url_for('login'))

    query = None
    if request.method == 'POST':
        query = request.form['search_query'] if 'search_query' in request.form else request.form.get('topic')
    return render_template('start.html', username=session['username'], query=query)

@app.route('/recommend', methods=['POST'])
def recommend():
    if 'username' not in session:
        return redirect(url_for('login'))

    topic = request.form.get('topic', 'inspirational')
    return render_template('recommend.html', username=session['username'], topic=topic)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            error = "Username already exists. Choose another."
        else:
            users[username] = password
            success = "Account created! You can now log in."

    return render_template('register.html', error=error, success=success)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


