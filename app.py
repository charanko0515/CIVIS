from flask import Flask, request, render_template, redirect
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads'


# =========================
# FUNÇÃO DE CONEXÃO
# =========================
def conectar():
    return sqlite3.connect('database.py')


# =========================
# PÁGINAS
# =========================
@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/denuncia')
def denuncia():
    return render_template('denuncia.html')


# =========================
# CADASTRO DE USUÁRIO
# =========================
@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():

    cpf = request.form.get('cpf')
    nome = request.form.get('name')
    email = request.form.get('email')
    senha = request.form.get('senha')

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuario (cpf, name, email, password)
        VALUES (?, ?, ?, ?)
    """, (cpf, nome, email, senha))

    conexao.commit()
    conexao.close()

    return redirect('/login')


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['POST'])
def fazer_login():

    cpf = request.form.get('cpf')
    senha = request.form.get('senha')

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM usuario
        WHERE cpf = ? AND password = ?
    """, (cpf, senha))

    usuario = cursor.fetchone()

    conexao.close()

    if usuario:
        return redirect('/')

    return 'CPF ou senha inválidos'


# =========================
# RECEBER DENÚNCIA
# =========================
@app.route('/receber_denuncia', methods=['POST'])
def receber_denuncia():

    categoria = request.form.get('categoria')
    descricao = request.form.get('descricao')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    foto = request.files.get('foto')

    # cria pasta uploads
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # salva foto
    foto_caminho = f'{UPLOAD_FOLDER}/{foto.filename}'
    foto.save(foto_caminho)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO denuncias
        (categoria, descricao, latitude, longitude, foto_caminho, data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        categoria,
        descricao,
        latitude,
        longitude,
        foto_caminho,
        datetime.now()
    ))

    protocolo = cursor.lastrowid

    conexao.commit()
    conexao.close()

    return render_template(
        'confirmacao.html',
        protocolo=protocolo,
        categoria=categoria,
        descricao=descricao,
        latitude=latitude,
        longitude=longitude,
        data=datetime.now().strftime('%d/%m/%Y %H:%M')
    )


# =========================
# INICIAR SERVIDOR
# =========================
if __name__ == '__main__':
    app.run(debug=True)