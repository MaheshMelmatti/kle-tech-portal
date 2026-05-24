from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'kletch-secret-2025'

# Simple in-memory user store (replace with DB in production)
users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usn = request.form['usn'].strip().upper()
        password = request.form['password']
        user = users.get(usn)
        if user and user['password'] == password:
            session['usn'] = usn
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid USN or Password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name       = request.form['name'].strip()
        usn        = request.form['usn'].strip().upper()
        department = request.form['department']
        email      = request.form['email'].strip()
        password   = request.form['password']
        confirm    = request.form['confirm_password']

        if password != confirm:
            return render_template('register.html', error='Passwords do not match.')
        if usn in users:
            return render_template('register.html', error='USN already registered.')

        users[usn] = {'name': name, 'department': department, 'email': email, 'password': password}
        return render_template('login.html', success='Registration successful! Please login.')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'usn' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['name'], usn=session['usn'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
