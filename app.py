from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'adriano',
    'database': 'DB_ATIVIDADE'
}

# Função para conectar ao banco de dados
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        print("Conexão com banco de dados estabelecida com sucesso!")
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome']
        senha = request.form['senha']
        tipo_usuario = request.form['tipo_usuario']
        
        # Conecta ao banco de dados
        conn = get_db_connection()
        if not conn:
            flash('Erro ao conectar ao banco de dados')
            return render_template('login.html', error='Erro de conexão')
        
        cursor = conn.cursor(dictionary=True)
        table = 'ADMINISTRADOR' if tipo_usuario == 'administrador' else 'FUNCIONARIO'
        query = f"SELECT * FROM {table} WHERE nome_usuario = %s AND senha_usuario = %s"
        cursor.execute(query, (nome_usuario, senha))
        usuario = cursor.fetchone()

        if usuario:
            # Login bem-sucedido, salva informações da sessão
            session['logged_in'] = True
            session['user_id'] = usuario['id_usuario']
            session['user_type'] = tipo_usuario
            session['user_name'] = usuario['nome_usuario']
            # Redireciona com base no tipo de usuário
            return redirect(url_for('telaadm' if tipo_usuario == 'administrador' else 'telafunc'))
        else:
            flash('Usuário ou senha inválidos')
            return render_template('login.html', error='Usuário ou senha inválidos')

        cursor.close()
        conn.close()

    return render_template('login.html')

# Rota para a página do administrador
@app.route('/telaadm')
def telaadm():
    if not session.get('logged_in') or session.get('user_type') != 'administrador':
        return redirect(url_for('login'))
    return render_template('telaadm.html', user_name=session.get('user_name'))

# Rota para a página do funcionário
@app.route('/telafunc')
def telafunc():
    if not session.get('logged_in') or session.get('user_type') != 'funcionario':
        return redirect(url_for('login'))
    return render_template('telafunc.html', user_name=session.get('user_name'))

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)









