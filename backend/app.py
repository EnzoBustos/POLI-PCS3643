from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid

app = Flask(__name__, template_folder='../', static_folder='../assets')
app.secret_key = 'labsoft'  # chave secreta segura
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def connect_db():
    return psycopg2.connect(
        host="200.144.245.12",      # IP correto do servidor
        port="65432",               # Porta correta para o PostgreSQL
        database="db_grupo01",      # Nome do banco de dados
        user="u_grupo01",           # usuário do PostgreSQL
        password="grupo01"          # senha do PostgreSQL
    )

# Modelo de Usuário


class User(UserMixin):
    def __init__(self, user_id, email, username, password, location_id):
        self.id = user_id
        self.email = email
        self.username = username
        self.password = password
        self.location_id = location_id


@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return User(user['user_id'], user['email'], user['username'], user['password'], user['location_id'])
    return None

# Formulários


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class RegisterForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[
                           DataRequired(), Length(min=4, max=25)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[
                             DataRequired(), Length(min=6)])
    submit = SubmitField('Registrar')

# Rotas de Autenticação


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s",
                       (form.email.data,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Verifica se o usuário existe e a senha está correta
        if user and check_password_hash(user['password'], form.password.data):
            user_obj = User(user['user_id'], user['email'],
                            user['username'], user['password'], user['location_id'])
            login_user(user_obj)
            return redirect(url_for('auth_index'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
            # Redireciona para a página de login novamente em caso de erro
            return render_template('login.html', form=form)

    # Renderiza o template de login com o formulário
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Verificar se o e-mail ou nome de usuário já existe
            cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s",
                           (form.email.data, form.username.data))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('E-mail ou nome de usuário já estão em uso.')
                return render_template('register.html', form=form)

            # Inserir novo usuário com senha hash
            hashed_password = generate_password_hash(
                form.password.data, method='pbkdf2:sha256')
            cursor.execute("""
    INSERT INTO users (user_id, email, username, password, created_at, updated_at, user_type)
    VALUES (%s, %s, %s, %s, NOW(), NOW(), %s)
""", (str(uuid.uuid4()), form.email.data, form.username.data, hashed_password, 'user'))

            conn.commit()

            flash('Registrado com sucesso! Faça login.')
            return redirect(url_for('login'))

        finally:
            cursor.close()
            conn.close()

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Rotas existentes


@app.route('/')
def index():
    return render_template('index.html')

# Exemplo de rota protegida


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

# Rotas para dados específicos


def get_data_from_table(table_name):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM {table_name}")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


@app.route('/mosquito')
def get_mosquito_info():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT * FROM articles WHERE title = 'Aedes aegypti' OR article_id = 'mosquito_01'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(result)

# Outras rotas de exemplo


@app.route('/research')
def get_research_info():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT * FROM research WHERE title = 'Pesquisa sobre o mosquito'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(result)

# Rotas para todas as tabelas


@app.route('/articles')
def get_articles():
    return jsonify(get_data_from_table('articles'))


@app.route('/category')
def get_category():
    return jsonify(get_data_from_table('category'))

# Continue com as outras rotas específicas que você listou


@app.route('/auth_index')
def auth_index():
    return render_template('auth_index.html')


if __name__ == "__main__":
    app.run(debug=True)
