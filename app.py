from flask import Flask, request, render_template, redirect
from datetime import datetime
import sqlite3, os

app = Flask(__name__)

def db(query, params=()):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    lastrow = cur.lastrowid
    con.close()
    return lastrow

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        db("INSERT INTO usuario (name,cpf, email, password) VALUES (?, ?, ?, ?)",
           (request.form.get('nome'), request.form.get('email'), request.form.get('senha')))
        return redirect('/login')
    return render_template('cadastro.html')

@app.route('/receber_denuncia', methods=['POST'])
def receber_denuncia():
    foto = request.files.get('foto')
    os.makedirs('static/uploads', exist_ok=True)
    foto_caminho = f'static/uploads/{foto.filename}'
    foto.save(foto_caminho)

    protocolo = db(
        "INSERT INTO denuncias (categoria, latitude, longitude, foto_caminho, descriacao) VALUES (?, ?, ?, ?, ?)",
        (request.form.get('categoria'), request.form.get('latitude'), request.form.get('longitude'), foto_caminho, request.form.get('descriacao'))
    )

    return render_template('confirmacao.html',
        protocolo=protocolo,
        categoria=request.form.get('categoria'),
        latitude=request.form.get('latitude'),
        longitude=request.form.get('longitude'),
        data=datetime.now().strftime('%d/%m/%Y %H:%M')
    )

if __name__ == '__main__':
    app.run(debug=True)