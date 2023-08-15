from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'alura'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'game_library'
    )

db = SQLAlchemy(app)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    platform = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Users(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def index():
    list = Games.query.order_by(Games.id)
    return render_template('list.html', title='Games', games=list)

@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('new')))
    return render_template('new.html', title='New game')

@app.route('/create', methods=['POST',])
def create():
    name = request.form['name']
    category = request.form['category']
    platform = request.form['platform']

    game = Games.query.filter_by(nome=nome).first()

    if game:
        flash('Game already added')
        return redirect(url_for('index'))

    new_game = Games(name=name, category=category, platform=platform)
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)

@app.route('/authenticate', methods=['POST',])
def authenticate():
    user = Users.query.filter_by(nickname=request.form['user']).first()
    if user:
        if request.form['password'] == user.password:
            session['logged_user'] = user.nickname
            flash(user.nickname + ' logado com sucesso!')
            next_page = request.form['next']
            return redirect(next_page)
    else:
        flash('User not logged in.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('Logged out successfully')
    return redirect(url_for('index'))

app.run(debug=True)