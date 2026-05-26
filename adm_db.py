import sqlite3

def conectar():
    return sqlite3.connect('database.db')

def buscar_ocorrencias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT categoria, latitude, longitude FROM denuncias")
    ocorrencias = [{"categoria": r[0], "lat": r[1], "lng": r[2]} for r in cursor.fetchall()]
    conexao.close()
    return ocorrencias

def buscar_feed_dados(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    
    # Busca todas as denúncias com contagem de ups
    cursor.execute("""
        SELECT d.id, d.categoria, d.descricao, d.latitude, d.longitude,
               d.foto_caminho, d.data_registro, COUNT(u.id) as total_ups
        FROM denuncias d
        LEFT JOIN ups u ON u.denuncia_id = d.id
        GROUP BY d.id
        ORDER BY total_ups DESC, d.data_registro DESC
    """)
    colunas = ['id','categoria','descricao','latitude','longitude','foto_caminho','data_registro','total_ups']
    denuncias = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    
    # Busca os ups do usuário logado
    cursor.execute("SELECT denuncia_id FROM ups WHERE usuario_id = ?", (usuario_id,))
    ups_dados = {row[0] for row in cursor.fetchall()}
    
    conexao.close()
    return denuncias, ups_dados

def buscar_perfil_dados(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    
    # Busca dados do usuário
    cursor.execute("SELECT * FROM usuario WHERE id = ?", (usuario_id,))
    colunas_u = ['id','cpf','nome','email','senha','data_criacao']
    usuario = dict(zip(colunas_u, cursor.fetchone()))
    
    # Busca denúncias
    cursor.execute("SELECT id, categoria, descricao, latitude, longitude, foto_caminho, data_registro FROM denuncias ORDER BY data_registro DESC")
    colunas_d = ['id','categoria','descricao','latitude','longitude','foto_caminho','data_registro']
    denuncias = [dict(zip(colunas_d, row)) for row in cursor.fetchall()]
    
    conexao.close()
    return usuario, denuncias

def cadastrar_usuario(cpf, nome, email, senha):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuario (cpf, nome, email, senha) VALUES (?, ?, ?, ?)", (cpf, nome, email, senha))
    conexao.commit()
    conexao.close()

def verificar_login(cpf, senha):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuario WHERE cpf = ? AND senha = ?", (cpf, senha))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario

def inserir_denuncia(categoria, descricao, latitude, longitude, foto_caminho):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO denuncias (categoria, descricao, latitude, longitude, foto_caminho)
        VALUES (?, ?, ?, ?, ?)
    """, (categoria, descricao, latitude, longitude, foto_caminho))
    protocolo = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return protocolo

def alternar_up(denuncia_id, usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM ups WHERE denuncia_id = ? AND usuario_id = ?", (denuncia_id, usuario_id))
    
    if cursor.fetchone():
        cursor.execute("DELETE FROM ups WHERE denuncia_id = ? AND usuario_id = ?", (denuncia_id, usuario_id))
    else:
        cursor.execute("INSERT INTO ups (denuncia_id, usuario_id) VALUES (?, ?)", (denuncia_id, usuario_id))
        
    conexao.commit()
    conexao.close()