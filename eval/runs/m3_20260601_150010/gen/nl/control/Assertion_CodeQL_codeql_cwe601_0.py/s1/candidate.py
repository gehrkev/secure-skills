from flask import Flask, request, session, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Mock database - replace with actual database calls
# In production, use a proper ORM like SQLAlchemy
USERS_DB = {
    'user1': 'password1',
    'user2': 'password2',
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists and password is correct
        if username and password and username in USERS_DB and USERS_DB[username] == password:
            # Create session for valid user
            session['user_id'] = username
            session['logged_in'] = True

            # Redirect to next URL or default to index
            next_url = request.args.get('next') or url_for('index')
            return redirect(next_url)
        else:
            # Authentication failed - render login.html with error
            return render_template('login.html', error='Authentication failed')

    # GET request - show login form
    return render_template('login.html')


@app.route('/')
def index():
    return 'Home Page'


if __name__ == '__main__':
    app.run(debug=True)
