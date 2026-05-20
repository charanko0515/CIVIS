from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

#pega os dados da pagina de cadastro
@app.route('/cadastro', methods=['POST'])
def getCadastro():
    #pega as dados e aloca em cada variavel

    #cpf = request.form.get('') #aqui esta o novo atributo que tem que ser alterado 
    name = request.form.get('nome')
    email = request.form.get('email')
    password = request.form.get('senha')
    print(f'esse e seus dados {name} {email} {password}')

    #faz a conexao denovo com o banco de dados 
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    
    #insere no banco de dados
    cursor.execute("""
        INSERT INTO usuario (name, email, password)
        VALUES (?, ?, ?)
    """, (name, email, password))

    conexao.commit()
    conexao.close()

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)