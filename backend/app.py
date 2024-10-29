from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
app = Flask(__name__)


def connect_db():
    return psycopg2.connect(
        host="200.144.245.12",      # Substitua pelo IP correto do seu servidor
        port="65432",               # Porta correta para o PostgreSQL
        database="db_grupo01",      # Nome do banco de dados
        user="u_grupo01",         # Seu usuário do PostgreSQL
        password="grupo01"        # Sua senha do PostgreSQL
    )


CORS(app)
# Função genérica para buscar dados de qualquer tabela


def get_data_from_table(table_name):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM {table_name}")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Rota para obter informações específicas sobre o mosquito
@app.route('/mosquito')
def get_mosquito_info():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT * FROM articles WHERE title = 'Aedes aegypti' OR article_id = 'mosquito_01'")
    result = cursor.fetchone()  # Obtém o primeiro (e único) resultado
    cursor.close()
    conn.close()
    return jsonify(result)

# Rota para obter informações de pesquisas (exemplo)


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

# Rota para obter informações de notícias (exemplo)


@app.route('/news')
def get_news_info():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT * FROM news WHERE title = 'Notícia sobre o mosquito'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(result)

# Rota para obter informações de reports (exemplo)


@app.route('/report')
def get_report_info():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT * FROM reports WHERE report_id = 'report_mosquito'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(result)
# Rotas para cada tabela


@app.route('/articles')
def get_articles():
    return jsonify(get_data_from_table('articles'))


@app.route('/articles_comments')
def get_articles_comments():
    return jsonify(get_data_from_table('articles_comments'))


@app.route('/articles_historic')
def get_articles_historic():
    return jsonify(get_data_from_table('articles_historic'))


@app.route('/category')
def get_category():
    return jsonify(get_data_from_table('category'))


@app.route('/deptos')
def get_deptos():
    return jsonify(get_data_from_table('deptos'))


@app.route('/funcionarios')
def get_funcionarios():
    return jsonify(get_data_from_table('funcionarios'))


@app.route('/funcproj')
def get_funcproj():
    return jsonify(get_data_from_table('funcproj'))


@app.route('/locations')
def get_locations():
    return jsonify(get_data_from_table('locations'))


@app.route('/news')
def get_news():
    return jsonify(get_data_from_table('news'))


@app.route('/news_comments')
def get_news_comments():
    return jsonify(get_data_from_table('news_comments'))


@app.route('/news_historic')
def get_news_historic():
    return jsonify(get_data_from_table('news_historic'))


@app.route('/projetos')
def get_projetos():
    return jsonify(get_data_from_table('projetos'))


@app.route('/reports')
def get_reports():
    return jsonify(get_data_from_table('reports'))


@app.route('/research')
def get_research():
    return jsonify(get_data_from_table('research'))


@app.route('/research_comments')
def get_research_comments():
    return jsonify(get_data_from_table('research_comments'))


@app.route('/research_historic')
def get_research_historic():
    return jsonify(get_data_from_table('research_historic'))


@app.route('/resources')
def get_resources():
    return jsonify(get_data_from_table('resources'))


@app.route('/users')
def get_users():
    return jsonify(get_data_from_table('users'))


if __name__ == "__main__":
    app.run(debug=True)
