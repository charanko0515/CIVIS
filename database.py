import sqlite3

conexao = sqlite3.connect('database.db')
cursor = conexao.cursor()
    # 1. Tabela de Usuários
cursor.execute("""
     CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpf TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

 # 2. Tabela de Denúncias (Agora com a coluna usuario_id)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS denuncias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        descricao TEXT,
        latitude TEXT,
        longitude TEXT,
        foto_caminho TEXT,
        data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        usuario_id INTEGER,
        FOREIGN KEY(usuario_id) REFERENCES usuario(id)
    )
""")

    # 3. Tabela de Ups (Curtidas)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        denuncia_id INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        data_up DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(denuncia_id) REFERENCES denuncias(id),
        FOREIGN KEY(usuario_id) REFERENCES usuario(id)
    )
""")

conexao.commit()
conexao.close()
print("Banco de dados recriado com sucesso! Coluna usuario_id adicionada.")