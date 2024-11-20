import sqlite3

def criar_banco():
    # Conectar ao banco de dados (será criado se não existir)
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # Comando SQL para criar a tabela 'usuarios' com o campo CPF
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            CPF TEXT NOT NULL
        )
    ''')

    # Commit para garantir que a operação seja salva
    conn.commit()
    
    # Fechar a conexão
    conn.close()

# Executar a função para criar o banco de dados
criar_banco()
