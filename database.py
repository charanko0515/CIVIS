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

# 2. Tabela de Denúncias
cursor.execute("""
    CREATE TABLE IF NOT EXISTS denuncias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descricao TEXT,
        latitude TEXT,
        longitude TEXT,
        foto_caminho TEXT,
        anonimo INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'Aberta',
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

# Migracoes: adiciona colunas novas sem apagar dados existentes
migracoes = [
    ("titulo",   "ALTER TABLE denuncias ADD COLUMN titulo TEXT NOT NULL DEFAULT 'Sem título'"),
    ("anonimo",  "ALTER TABLE denuncias ADD COLUMN anonimo INTEGER NOT NULL DEFAULT 0"),
    ("status",   "ALTER TABLE denuncias ADD COLUMN status TEXT NOT NULL DEFAULT 'Aberta'"),
]

colunas_existentes = {row[1] for row in cursor.execute("PRAGMA table_info(denuncias)")}

for coluna, sql in migracoes:
    if coluna not in colunas_existentes:
        cursor.execute(sql)
        print(f"Coluna '{coluna}' adicionada com sucesso.")

conexao.commit()
conexao.close()
print("Banco de dados atualizado com sucesso!")
