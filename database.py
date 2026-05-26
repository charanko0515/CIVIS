import sqlite3

conexao = sqlite3.connect('database.db')
cursor = conexao.cursor()

# Cria a tabela denuncias
cursor.execute('''
CREATE TABLE IF NOT EXISTS denuncias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    foto_caminho TEXT NOT NULL,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    descricao TEXT NOT NULL,
    protocolo 
    status
)
''')

# Cria a tabela usuario
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpf TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL, 
    senha TEXT NOT NULL,
    data_criacão DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

#Cria a tabela ups
cursor.execute('''
CREATE TABLE IF NOT EXISTS ups (
    denuncia_id INTEGER,
    usuario_id INTEGER,
    
    PRIMARY KEY (denuncia_id, usuario_id),
    
    FOREIGN KEY (denuncia_id) REFERENCES denuncias(id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
)
''')

# Salva as alterações e fecha a conexão
conexao.commit()
conexao.close()

print("Banco de dados 'database.db' criado e pronto para uso!")