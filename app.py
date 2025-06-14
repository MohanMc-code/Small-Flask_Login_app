from flask import Flask, render_template, request, redirect, url_for
from models import User ,db

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login',methods=['POST','GET'])
def login():
    error=None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and request.form['password']== user.password:
            return render_template('success.html',username=request.form['username'])
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)
@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            error = 'Username already exists. Please choose a different one.'
        else:      
            new_user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')
if __name__== '__main__':
    app.run(host='0.0.0.0', port=5000)