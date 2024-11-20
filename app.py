from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'adriano',
    'database': 'DB_ATIVIDADE'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        print("Conexão com banco de dados estabelecida com sucesso!")
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome']
        senha = request.form['senha']
        tipo_usuario = request.form['tipo_usuario']
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                flash('Erro ao conectar ao banco de dados')
                return render_template('login.html')
            
            cursor = conn.cursor(dictionary=True)
            table = 'ADMINISTRADOR' if tipo_usuario == 'administrador' else 'FUNCIONARIO'
            
            query = f"SELECT * FROM {table} WHERE nome_usuario = %s AND senha_usuario = %s"
            cursor.execute(query, (nome_usuario, senha))
            usuario = cursor.fetchone()

            if usuario:
                session['logged_in'] = True
                session['user_id'] = usuario['id_usuario']
                session['user_type'] = tipo_usuario
                session['user_name'] = usuario['nome_usuario']
                return redirect(url_for('telaadm' if tipo_usuario == 'administrador' else 'telafunc'))
            else:
                return render_template('login.html')

        except mysql.connector.Error as err:
            print(f'Erro no banco de dados: {err}')
            return render_template('login.html')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('login.html')

@app.route('/telaadm')
def telaadm():
    if not session.get('logged_in') or session.get('user_type') != 'administrador':
        return redirect(url_for('login'))
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro ao conectar ao banco de dados')
            return redirect(url_for('login'))
        
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT id_usuario, nome_usuario, data_cadastro_usuario FROM FUNCIONARIO"
        cursor.execute(query)
        funcionarios = cursor.fetchall()
        
        return render_template('telaadm.html', 
                             user_name=session.get('user_name'),
                             funcionarios=funcionarios)
    
    except mysql.connector.Error as err:
        flash(f'Erro ao buscar funcionários: {err}')
        return redirect(url_for('login'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/cadastrar_funcionario', methods=['POST'])
def cadastrar_funcionario():
    if not session.get('logged_in') or session.get('user_type') != 'administrador':
        return redirect(url_for('login'))
    
    nome = request.form['nome']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']
    
    if senha != confirmar_senha:
        flash('As senhas não coincidem')
        return redirect(url_for('telaadm'))
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro ao conectar ao banco de dados')
            return redirect(url_for('telaadm'))
        
        cursor = conn.cursor()
        
        query = """
        INSERT INTO FUNCIONARIO (nome_usuario, senha_usuario, data_cadastro_usuario)
        VALUES (%s, %s, NOW())
        """
        cursor.execute(query, (nome, senha))
        conn.commit()
        
        flash('Funcionário cadastrado com sucesso!')
        return redirect(url_for('telaadm'))
    
    except mysql.connector.Error as err:
        flash(f'Erro ao cadastrar funcionário: {err}')
        return redirect(url_for('telaadm'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/deletar_funcionario/<int:id>')
def deletar_funcionario(id):
    if not session.get('logged_in') or session.get('user_type') != 'administrador':
        return redirect(url_for('login'))
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro ao conectar ao banco de dados')
            return redirect(url_for('telaadm'))
        
        cursor = conn.cursor()
        query = "DELETE FROM FUNCIONARIO WHERE id_usuario = %s"
        cursor.execute(query, (id,))
        conn.commit()
        
        flash('Funcionário deletado com sucesso!')
        return redirect(url_for('telaadm'))
    
    except mysql.connector.Error as err:
        flash(f'Erro ao deletar funcionário: {err}')
        return redirect(url_for('telaadm'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/telafunc')
def telafunc():
    if not session.get('logged_in') or session.get('user_type') != 'funcionario':
        return redirect(url_for('login'))
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro ao conectar ao banco de dados')
            return redirect(url_for('login'))
        
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM PRODUTOS"
        cursor.execute(query)
        produtos = cursor.fetchall()
        
        return render_template('telafunc.html', 
                             user_name=session.get('user_name'),
                             produtos=produtos)
    
    except mysql.connector.Error as err:
        flash(f'Erro ao buscar produtos: {err}')
        return redirect(url_for('login'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    if not session.get('logged_in') or session.get('user_type') != 'funcionario':
        return redirect(url_for('login'))
    
    marca = request.form['marca']
    nome = request.form['nome']
    codigo = request.form['codigo']
    quantidade = request.form['quantidade']
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro ao conectar ao banco de dados')
            return redirect(url_for('telafunc'))
        
        cursor = conn.cursor()
        
        # Verificar se o código já existe
        cursor.execute("SELECT cod_produto FROM PRODUTOS WHERE cod_produto = %s", (codigo,))
        if cursor.fetchone():
            flash('Já existe um produto com este código!')
            return redirect(url_for('telafunc'))
        
        query = """
        INSERT INTO PRODUTOS (marca_produto, nome_produto, cod_produto, qtd_estoque)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (marca, nome, codigo, quantidade))
        conn.commit()
        
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('telafunc'))
    
    except mysql.connector.Error as err:
        flash(f'Erro ao cadastrar produto: {err}')
        return redirect(url_for('telafunc'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/atualizar_quantidade/<int:id>', methods=['POST'])
def atualizar_quantidade(id):
    if not session.get('logged_in') or session.get('user_type') != 'funcionario':
        return redirect(url_for('login'))
    
    nova_quantidade = request.form.get('quantidade')
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro ao conectar ao banco de dados')
            return redirect(url_for('telafunc'))
        
        cursor = conn.cursor()
        query = "UPDATE PRODUTOS SET qtd_estoque = %s WHERE id_produto = %s"
        cursor.execute(query, (nova_quantidade, id))
        conn.commit()
        
        flash('Quantidade atualizada com sucesso!')
        return redirect(url_for('telafunc'))
    
    except mysql.connector.Error as err:
        flash(f'Erro ao atualizar quantidade: {err}')
        return redirect(url_for('telafunc'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)