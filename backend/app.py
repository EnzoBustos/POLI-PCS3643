from datetime import datetime
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
import requests
from flask_login import current_user
from datetime import datetime

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
    def __init__(self, user_id, email, username, password, location_id, user_type):
        self.id = user_id
        self.email = email
        self.username = username
        self.password = password
        self.location_id = location_id
        self.user_type = user_type  # Adicione o atributo user_type


@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return User(user['user_id'], user['email'], user['username'], user['password'], user['location_id'], user['user_type'])
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
            user_obj = User(
                user['user_id'],
                user['email'],
                user['username'],
                user['password'],
                user['location_id'],
                user['user_type']  # Adiciona o user_type ao criar o objeto
            )
            login_user(user_obj)
            return redirect(url_for('auth_index'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
            return render_template('login.html', form=form)

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


def fetch_dengue_news():
    api_key = "17f5dd0c4aca476f9ee1d9a340764639"
    url = f"https://newsapi.org/v2/everything?q=dengue&apiKey={api_key}"
    response = requests.get(url)

    # Verifica se a API retornou sucesso
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        print("Artigos retornados pela API:", articles)  # Debug
    else:
        flash("Erro ao buscar notícias da API.", "danger")
        return []

    conn = connect_db()
    cursor = conn.cursor()

    # Categoria padrão
    default_category_id = "id_da_categoria_padrao"
    category_name = "Dengue"

    # Verifica se a categoria padrão existe
    cursor.execute("SELECT 1 FROM category WHERE category_id = %s",
                   (default_category_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO category (category_id, name) VALUES (%s, %s)",
                       (default_category_id, category_name))

    # Insere artigos no banco de dados
    for article in articles:
        title = article.get('title')
        url = article.get('url', "")  # Captura o campo 'url'

        if not title or not url:  # Certifica-se de que o título e a URL existem
            continue

        summary = article.get('description', "")
        content = article.get('content', "")
        created_at = updated_at = datetime.now()
        new_id = str(uuid.uuid4())

        if not title or not url:  # Certifique-se de que o título e a URL existem
            continue

        # Atualiza a notícia no banco de dados com a URL
        cursor.execute("""
            UPDATE news
            SET url = %s
            WHERE title = %s
        """, (url, title))

        # Verifica se o título já existe no banco de dados
        cursor.execute("SELECT 1 FROM news WHERE title = %s", (title,))
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO news (new_id, title, summary, content, url, created_at, updated_at, user_id, category_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (new_id, title, summary, content, url, created_at, updated_at, None, default_category_id))

    conn.commit()
    cursor.close()
    conn.close()

    return articles


def get_articles_from_db():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM news ORDER BY created_at DESC")
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    print("Artigos recuperados do banco de dados:", articles)  # Debug
    return articles


def get_news_id_by_title(title):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT news_id FROM news WHERE title = %s", (title,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


@app.route('/dengue_news')
def dengue_news():
    # Busca notícias na API e as insere no banco
    fetch_dengue_news()

    # Recupera notícias do banco de dados
    db_articles = get_articles_from_db()
    print("Artigos recuperados do banco de dados:", db_articles)

    # Adiciona comentários (se o usuário estiver logado)
    for article in db_articles:
        article_id = article['new_id']
        article['comments'] = get_comments(article_id)

    return render_template('dengue_news.html', articles=db_articles)


def get_comments(article_id):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT news_comments.content, users.username
        FROM news_comments
        JOIN users ON news_comments.user_id = users.user_id
        WHERE news_comments.new_id = %s
        ORDER BY news_comments.created_at DESC
    """, (article_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments


@app.route('/add-comment/<string:article_id>', methods=['POST'])
@login_required
def add_comment(article_id):
    content = request.form.get('content')
    user_id = current_user.id  # ID do usuário logado
    comment_id = str(uuid.uuid4())

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO news_comments (comment_id, content, created_at, updated_at, user_id, new_id, upvotes, downvotes)
        VALUES (%s, %s, NOW(), NOW(), %s, %s, 0, 0)
    """, (comment_id, content, user_id, article_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Comentário adicionado com sucesso!", "success")
    return redirect(url_for('dengue_news'))


@app.route('/profile')
@login_required
def profile():
    # Obtenha as informações do usuário logado
    user_info = {
        "username": current_user.username,
        "email": current_user.email,
        "user_type": current_user.user_type,  # Identifica se é admin ou normal
    }

    # Renderize um template diferente para admins, se necessário
    if current_user.user_type == "admin":
        return render_template('admin_profile.html', user_info=user_info)
    else:
        return render_template('user_profile.html', user_info=user_info)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET username = %s, email = %s
            WHERE user_id = %s
        """, (username, email, current_user.id))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user_info=current_user)


@app.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Insere o artigo no banco de dados
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO articles (title, content, user_id, is_approved)
            VALUES (%s, %s, %s, 'FALSE')
        """, (title, content, current_user.id))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Artigo criado e enviado para aprovação!", "success")
        return redirect(url_for('create_article'))

    return render_template('create_article.html')


@app.route('/admin/articles', methods=['GET', 'POST'])
@login_required
def admin_articles():
    if current_user.user_type != 'admin':  # Certifica que só admins acessam
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('index'))

    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Busca os artigos que ainda não foram aprovados
    cursor.execute("SELECT * FROM articles WHERE is_approved = 'FALSE'")
    pending_articles = cursor.fetchall()

    if request.method == 'POST':
        article_id = request.form.get('article_id')
        # Identifica se é aprovar ou rejeitar
        action = request.form.get('action')

        if action == 'approve':
            # Aprova o artigo no banco de dados
            cursor.execute("""
                UPDATE articles SET is_approved = 'TRUE', updated_at = NOW() WHERE article_id = %s
            """, (article_id,))
            flash("Artigo aprovado com sucesso!", "success")
        elif action == 'reject':
            # Rejeita o artigo no banco de dados (altera status ou remove)
            cursor.execute("""
                UPDATE articles SET is_approved = 'REFUSED', updated_at = NOW() WHERE article_id = %s
            """, (article_id,))
            flash("Artigo rejeitado com sucesso!", "success")

        conn.commit()
        return redirect(url_for('admin_articles'))

    cursor.close()
    conn.close()
    return render_template('admin_articles.html', articles=pending_articles)


@app.route('/wiki')
def wiki():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Busca artigos aprovados
    cursor.execute("SELECT * FROM articles WHERE is_approved = 'TRUE'")
    approved_articles = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('wiki2.html', articles=approved_articles)


@app.route('/manage_users')
@login_required
def manage_users():
    if current_user.user_type != 'admin':
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('index'))

    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT user_id, username, email, user_type FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('manage_users.html', users=users)


@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    # Captura os dados do formulário
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    location = request.form.get('location')
    severity = request.form.get('severity')
    method = request.form.get('method')
    message = request.form.get('message')

    # Insere os dados no banco de dados
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints (name, email, phone, location, severity, method, message, is_resolved, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE, NOW())
    """, (name, email, phone, location, severity, method, message))
    conn.commit()
    cursor.close()
    conn.close()

    # Exibe uma mensagem de sucesso e redireciona
    flash("Sua denúncia foi enviada com sucesso. Obrigado!", "success")
    return redirect(url_for('complaint_form'))


@app.route('/complaint_form')
def complaint_form():
    return render_template('complaint_form.html')


@app.route('/admin/complaints', methods=['GET', 'POST'])
@login_required
def admin_complaints():
    if current_user.user_type != 'admin':  # Apenas admin pode acessar
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('index'))

    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Buscar denúncias não resolvidas
    cursor.execute("SELECT * FROM complaints WHERE is_resolved = FALSE")
    pending_complaints = cursor.fetchall()

    if request.method == 'POST':
        complaint_id = request.form.get('complaint_id')
        # Atualizar denúncia como resolvida
        cursor.execute("""
            UPDATE complaints SET is_resolved = TRUE WHERE complaint_id = %s
        """, (complaint_id,))
        conn.commit()
        flash("Denúncia marcada como resolvida!", "success")
        return redirect(url_for('admin_complaints'))

    cursor.close()
    conn.close()
    return render_template('admin_complaints.html', complaints=pending_complaints)


if __name__ == "__main__":
    app.run(debug=True)
