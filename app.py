from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:0000@localhost/rebeka'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'  # Chave secreta para sessão

db = SQLAlchemy(app)

class Rebeka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    modalidade = db.Column(db.String(50))
    salario = db.Column(db.Float)
    cpf = db.Column(db.String(20))
    rg = db.Column(db.String(20))
    endereco = db.Column(db.String(100))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    cep = db.Column(db.String(20))
    banco = db.Column(db.String(50))
    pix = db.Column(db.String(100))
    data_pagamento = db.Column(db.Date)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(20), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        if 'cpf' in request.form:  # Verifica se é uma submissão de cadastro
            cpf = request.form['cpf']
            username = request.form.get('username')
            password = request.form['password']

            # Verifica se o CPF já está cadastrado
            existing_user = Login.query.filter_by(cpf=cpf).first()
            if existing_user:
                return render_template('login.html', message='CPF já cadastrado. Por favor, tente novamente.')

            # Verifica se o campo 'username' foi preenchido
            if not username:
                return render_template('login.html', message='O campo "username" é obrigatório. Por favor, preencha-o.')

            # Cria um novo usuário no banco de dados
            new_user = Login(cpf=cpf, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            session['username'] = new_user.username
            return redirect('/index')
        else:  # Submissão do formulário de login
            username = request.form['username']
            password = request.form['password']

            user = Login.query.filter_by(username=username, password=password).first()

            if user:
                session['username'] = user.username
                return redirect('/index')
            else:
                return render_template('login.html', message='Username ou senha incorretos.')

    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Verifica o formulário de cadastro
        if 'cpf' in request.form and 'username' in request.form and 'password' in request.form:
            cpf = request.form['cpf']
            username = request.form['username']
            password = request.form['password']
            # Resto do código de cadastro...

    return render_template('cadastro.html')

@app.route('/index', methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        nome = request.form['nome']
        cargo = request.form['cargo']
        modalidade = request.form['modalidade']
        salario = float(request.form['salario'])
        cpf = request.form['cpf']
        rg = request.form['rg']
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        cep = request.form['cep']
        banco = request.form['banco']
        pix = request.form['pix']
        data_pagamento = request.form['data_pagamento']
        username = session['username']  # Obtém o username da sessão

        pessoa = Rebeka(
            nome=nome, cargo=cargo, modalidade=modalidade, salario=salario, cpf=cpf, rg=rg, endereco=endereco,
            bairro=bairro, cidade=cidade, cep=cep, banco=banco, pix=pix, data_pagamento=data_pagamento
        )

        db.session.add(pessoa)
        db.session.commit()

        return redirect('/index')
    else:
        pessoas = Rebeka.query.all()
        return render_template('index.html', pessoas=pessoas)

@app.route('/lista')
def lista():
    if 'username' not in session:
        return redirect('/login')
    pessoas = Rebeka.query.all()
    return render_template('lista.html', pessoas=pessoas)
    return redirect(url_for('login'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'username' not in session:
        return redirect('/login')
    pessoa = Rebeka.query.get(id)

    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.cargo = request.form['cargo']
        pessoa.modalidade = request.form['modalidade']
        pessoa.salario = float(request.form['salario'])
        pessoa.cpf = request.form['cpf']
        pessoa.rg = request.form['rg']
        pessoa.endereco = request.form['endereco']
        pessoa.bairro = request.form['bairro']
        pessoa.cidade = request.form['cidade']
        pessoa.cep = request.form['cep']
        pessoa.banco = request.form['banco']
        pessoa.pix = request.form['pix']
        pessoa.data_pagamento = request.form['data_pagamento']

        db.session.commit()

        return redirect(request.referrer)
    else:
        return render_template('edit.html', pessoa=pessoa)

@app.route('/pessoa/<int:id>')
def pessoa(id):
    if 'username' not in session:
        return redirect('/login')
    pessoa = Rebeka.query.get(id)
    return render_template('pessoa.html', pessoa=pessoa)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    pessoa = Rebeka.query.get(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect('/index')

@app.route('/voltar')
def voltar():
    return redirect('/login')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
