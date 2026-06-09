from flask import Flask, request, render_template, redirect, session
from werkzeug.security import check_password_hash
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Database setup
engine = create_engine('sqlite:///users.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_url = request.args.get('next', '/')

        db_session = Session()
        user = db_session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            db_session.close()
            return redirect(next_url)
        else:
            db_session.close()
            return render_template('login.html', error='Authentication failed')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
