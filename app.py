from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        CPF = request.form['CPF']
        
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, email, senha, CPF) VALUES (?, ?, ?, ?)", (nome, email, senha, CPF))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Erro: Usuário com esse email ou CPF já existe."
        finally:
            conn.close()
        
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            session['nome'] = usuario[1]
            session['email'] = usuario[2]
            session['CPF'] = usuario[4]
            return redirect(url_for('destinos'))
        else:
            erro = "Erro: Email ou senha incorretos. Verifique suas credenciais ou cadastre-se."
    return render_template('login.html', erro=erro)

@app.route('/destinos', methods=['GET', 'POST'])
def destinos():
    destinos = [
        {"partida": "Cuiabá", "destino": "Rio de Janeiro", "valor": 900},
        {"partida": "Cuiabá", "destino": "Salvador", "valor": 820},
        {"partida": "Cuiabá", "destino": "São Paulo", "valor": 970},
        {"partida": "Cuiabá", "destino": "Gramado", "valor": 1480},
        {"partida": "Cuiabá", "destino": "Belo Horizonte", "valor": 1430},
        {"partida": "Cuiabá", "destino": "Curitiba", "valor": 1300},
        {"partida": "Cuiabá", "destino": "Brasilia", "valor": 900},
        {"partida": "Cuiabá", "destino": "Presidente Prudente", "valor": 600},
        {"partida": "Cuiabá", "destino": "Santos o Melhor time do mundo", "valor": 400},
    ]
    if request.method == 'POST':
        partida = request.form['partida']
        destino = request.form['destino']
        valor = request.form['valor']
        data_compra = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        
        nome = session.get('nome')
        email = session.get('email')
        CPF = session.get('CPF')
        
        return render_template('comprovante.html', nome=nome, email=email, CPF=CPF, data_compra=data_compra, partida=partida, destino=destino, valor=valor)
    
    return render_template('destinos.html', destinos=destinos)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)