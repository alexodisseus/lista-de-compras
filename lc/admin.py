from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import model



admin = Blueprint('admin', __name__, url_prefix='/')


@admin.route('/', methods=['GET'])
def index():
    print(session)  # Isso mostrará o que está na sessão
    print("asd")
    if 'userid' in session:  # Verifica se o usuário está logado
        return redirect(url_for('itens.index'))  # Redireciona para listas.index
    return render_template('index.html')  # Se não estiver logado, renderiza a página inicial



@admin.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')

        print(f"Nome: {name}, Senha: {password}, Email: {email}")  # Debug

        if not name or not password or not email:
            flash('Nome, senha e email são obrigatórios.')
            return render_template('signup.html')

        if model.create_user(name, password, email ):
            flash('Usuário criado com sucesso!')
            return redirect(url_for('admin.login'))
        else:
            flash('Erro ao criar usuário.')

    return render_template('signup.html')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Captura o email
        password = request.form.get('password')

        print(f"Email: {email}, Senha: {password}")  # Debug

        if not email or not password:
            flash('Email e senha são obrigatórios.')
            return render_template('login.html')

        user = model.read_user(email)  # Busca pelo email

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['userid'] = user.id
            return redirect(url_for('admin.index'))

        flash('Email ou senha incorretos.')

    return render_template('login.html')


@admin.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    return redirect(url_for('admin.login'))

def configure(app):
    app.register_blueprint(admin)

