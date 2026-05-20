import sqlite3

conexao = sqlite3.connect('database.db')
cursor = conexao.cursor()

# Cria a tabela "denuncias" (Esta já estava perfeita!)
cursor.execute('''
CREATE TABLE IF NOT EXISTS denuncias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    foto_caminho TEXT NOT NULL,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    descriacao TEXT NOT NULL
)
''')

# Cria a tabela "usuario" (Corrigida aqui)
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER,
    name TEXT NOT NULL,
    email TEXT NOT NULL, 
    password TEXT NOT NULL
)
''')

# Salva as alterações e fecha a conexão
conexao.commit()
conexao.close()

print("Banco de dados 'database.db' criado e pronto para uso!")