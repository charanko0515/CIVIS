from flask import Flask, request, render_template, redirect, session as sessao
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "civis_chave_secreta"

# Disponibiliza nome_usuario em todos os templates automaticamente
@app.context_processor
def injetar_usuario():
    return {"nome_usuario": sessao.get("nome_usuario")}


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# FUNÇÃO DE CONEXÃO
# =========================
def conectar():
    return sqlite3.connect('database.db')


# =========================
# PÁGINAS
# =========================
@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/denuncia')
def denuncia():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT categoria, latitude, longitude FROM denuncias")
    ocorrencias = [{"categoria": r[0], "lat": r[1], "lng": r[2]} for r in cursor.fetchall()]
    conexao.close()
    return render_template('homepage.html', ocorrencias=ocorrencias)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/feed')
def feed():
    if not sessao.get('usuario_id'):
        return redirect('/login')
    conexao = conectar()
    cursor = conexao.cursor()
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
    cursor.execute("SELECT denuncia_id FROM ups WHERE usuario_id = ?", (sessao['usuario_id'],))
    ups_dados = {row[0] for row in cursor.fetchall()}
    conexao.close()
    return render_template('feed.html', denuncias=denuncias, ups_dados=ups_dados)


@app.route('/perfil')
def perfil():
    if not sessao.get('usuario_id'):
        return redirect('/login')
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id = ?", (sessao['usuario_id'],))
    colunas_u = ['id','cpf','nome','email','senha','data_criacao']
    usuario = dict(zip(colunas_u, cursor.fetchone()))
    cursor.execute("SELECT id, categoria, descricao, latitude, longitude, foto_caminho, data_registro FROM denuncias ORDER BY data_registro DESC")
    colunas_d = ['id','categoria','descricao','latitude','longitude','foto_caminho','data_registro']
    denuncias = [dict(zip(colunas_d, row)) for row in cursor.fetchall()]
    conexao.close()
    return render_template('perfil.html', usuario=usuario, denuncias=denuncias)


# =========================
# CADASTRO DE USUÁRIO
# =========================
@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    cpf   = request.form.get('cpf')
    nome  = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    conexao = conectar()
    cursor  = conexao.cursor()
    cursor.execute("INSERT INTO usuario (cpf, nome, email, senha) VALUES (?, ?, ?, ?)", (cpf, nome, email, senha))
    conexao.commit()
    conexao.close()
    return redirect('/login')


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['POST'])
def fazer_login():
    cpf   = request.form.get('cpf')
    senha = request.form.get('senha')
    conexao = conectar()
    cursor  = conexao.cursor()
    cursor.execute("SELECT * FROM usuario WHERE cpf = ? AND senha = ?", (cpf, senha))
    usuario = cursor.fetchone()
    conexao.close()
    if usuario:
        sessao["nome_usuario"] = usuario[2]  # índice 2 = coluna nome
        sessao["usuario_id"]   = usuario[0]  # índice 0 = coluna id
        return redirect('/feed')
    return 'CPF ou senha inválidos'


# =========================
# RECEBER DENÚNCIA
# =========================
@app.route('/receber_denuncia', methods=['POST'])
def receber_denuncia():
    categoria = request.form.get('categoria')
    descricao = request.form.get('descricao')
    latitude  = request.form.get('latitude')
    longitude = request.form.get('longitude')
    foto      = request.files.get('foto')
    foto_caminho = os.path.join(UPLOAD_FOLDER, foto.filename)
    foto.save(foto_caminho)
    conexao = conectar()
    cursor  = conexao.cursor()
    cursor.execute("""
        INSERT INTO denuncias (categoria, descricao, latitude, longitude, foto_caminho)
        VALUES (?, ?, ?, ?, ?)
    """, (categoria, descricao, latitude, longitude, f'static/uploads/{foto.filename}'))
    protocolo = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return render_template('confirmacao.html',
        protocolo=protocolo, categoria=categoria,
        latitude=latitude, longitude=longitude,
        data=datetime.now().strftime('%d/%m/%Y %H:%M')
    )


# =========================
# UP EM DENÚNCIA
# =========================
@app.route('/up/<int:denuncia_id>', methods=['POST'])
def dar_up(denuncia_id):
    if not sessao.get('usuario_id'):
        return redirect('/login')
    conexao = conectar()
    cursor  = conexao.cursor()
    cursor.execute("SELECT id FROM ups WHERE denuncia_id = ? AND usuario_id = ?", (denuncia_id, sessao['usuario_id']))
    if cursor.fetchone():
        cursor.execute("DELETE FROM ups WHERE denuncia_id = ? AND usuario_id = ?", (denuncia_id, sessao['usuario_id']))
    else:
        cursor.execute("INSERT INTO ups (denuncia_id, usuario_id) VALUES (?, ?)", (denuncia_id, sessao['usuario_id']))
    conexao.commit()
    conexao.close()
    return redirect('/feed')


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    sessao.clear()
    return redirect('/')


# =========================
# INICIAR SERVIDOR
# =========================
if __name__ == '__main__':
    app.run(debug=True)