from flask import Flask, render_template, request, redirect, url_for , session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'chave_secreta123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://seu_usuario:sua_senha@localhost/nome_do_seu_banco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(20), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form.get('nome')
    login = request.form.get('login')
    senha = request.form.get('senha')

    novo_usuario = Usuario(nome=nome, login=login, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/login', methods=['POST'])
def login():
    login_form = request.form.get('login')
    senha_form = request.form.get('senha')

    usuario = Usuario.query.filter_by(login=login_form).first()

    if usuario and usuario.senha == senha_form:
        session['usuario'] = usuario.nome
        return redirect(url_for('inicial'))
    
    return "Login inválido"


@app.route('/inicial')
def inicial():

    if 'usuario' not in session:
        return redirect(url_for('home'))

    return render_template('inicial.html', nome=session['usuario'])



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
