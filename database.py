import sqlite3

# Conecta ao arquivo do banco se não existir, ele cria automaticamente
conexao = sqlite3.connect('database.db')
cursor = conexao.cursor()

# Cria a tabela "denuncias" com os campos necessários para o MVP
cursor.execute('''
CREATE TABLE IF NOT EXISTS denuncias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    foto_caminho TEXT NOT NULL,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Salva as alterações e fecha a conexão
conexao.commit()
conexao.close()

print("Banco de dados 'banco.db' criado e pronto para uso!")