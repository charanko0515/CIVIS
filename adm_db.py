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

    cursor.execute("""
        SELECT d.id, d.titulo, d.categoria, d.descricao, d.latitude, d.longitude,
               d.foto_caminho, d.data_registro, d.status, d.anonimo,
               u.nome, COUNT(up.denuncia_id) as total_ups
        FROM denuncias d
        LEFT JOIN usuario u ON u.id = d.usuario_id
        LEFT JOIN ups up ON up.denuncia_id = d.id
        GROUP BY d.id
        ORDER BY total_ups DESC, d.data_registro DESC
    """)
    colunas = ['id','titulo','categoria','descricao','latitude','longitude','foto_caminho','data_registro','status','anonimo','nome_usuario','total_ups']
    denuncias = [dict(zip(colunas, row)) for row in cursor.fetchall()]

    cursor.execute("SELECT denuncia_id FROM ups WHERE usuario_id = ?", (usuario_id,))
    ups_dados = {row[0] for row in cursor.fetchall()}

    conexao.close()
    return denuncias, ups_dados


def buscar_perfil_dados(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuario WHERE id = ?", (usuario_id,))
    colunas_u = ['id','cpf','nome','email','senha','data_criacao']
    row = cursor.fetchone()
    usuario = dict(zip(colunas_u, row)) if row else None

    cursor.execute("""
        SELECT id, titulo, categoria, descricao, latitude, longitude, foto_caminho, data_registro, status, anonimo
        FROM denuncias
        WHERE usuario_id = ?
        ORDER BY data_registro DESC
    """, (usuario_id,))
    colunas_d = ['id','titulo','categoria','descricao','latitude','longitude','foto_caminho','data_registro','status','anonimo']
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


def inserir_denuncia(titulo, categoria, descricao, latitude, longitude, foto_caminho, anonimo=0, usuario_id=None):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO denuncias (titulo, categoria, descricao, latitude, longitude, foto_caminho, anonimo, status, usuario_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Aberta', ?)
    """, (titulo, categoria, descricao, latitude, longitude, foto_caminho, anonimo, usuario_id))
    protocolo = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return protocolo


def alternar_up(denuncia_id, usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT denuncia_id FROM ups WHERE denuncia_id = ? AND usuario_id = ?", (denuncia_id, usuario_id))
    if cursor.fetchone():
        cursor.execute("DELETE FROM ups WHERE denuncia_id = ? AND usuario_id = ?", (denuncia_id, usuario_id))
    else:
        cursor.execute("INSERT INTO ups (denuncia_id, usuario_id) VALUES (?, ?)", (denuncia_id, usuario_id))
    conexao.commit()
    conexao.close()