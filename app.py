from flask import Flask, request, render_template, redirect, session as sessao, jsonify, flash
import os
from datetime import datetime

# Aqui está a mágica: importando suas funções do banco de dados
import adm_db as db

app = Flask(__name__)
app.secret_key = "civis_chave_secreta"

@app.context_processor
def injetar_usuario():
    return {"nome_usuario": sessao.get("nome_usuario")}

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# PÁGINAS
# =========================
@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/denuncia')
def denuncia():
    # Chama a função isolada no db
    ocorrencias = db.buscar_ocorrencias()
    return render_template('denuncia.html', ocorrencias=ocorrencias)


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
        
    # Busca os dados estruturados do banco
    denuncias, ups_dados = db.buscar_feed_dados(sessao['usuario_id'])
    return render_template('feed.html', denuncias=denuncias, ups_dados=ups_dados)


@app.route('/perfil')
def perfil():
    if not sessao.get('usuario_id'):
        return redirect('/login')
        
    usuario, denuncias = db.buscar_perfil_dados(sessao['usuario_id'])
    if not usuario:
        sessao.clear()
        return redirect('/login')
    return render_template('perfil.html', usuario=usuario, denuncias=denuncias)


# =========================
# CADASTRO DE USUÁRIO
# =========================
@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario_rota():
    cpf   = request.form.get('cpf')
    nome  = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    # 1. Remove pontos e traços para validar apenas os números
    cpf_limpo = cpf.replace('.', '').replace('-', '').strip()
    
    # 2. VALIDAÇÃO DO CPF: Se não tiver 11 números ou se conter letras
    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
        flash('CPF inválido! O campo deve conter exatamente 11 números.', 'danger')
        return redirect('/cadastro') # Mandamos de volta para a página de cadastro
    
    # 3. Se o CPF for válido, tenta salvar no banco de dados
    try:
        # Passamos o 'cpf_limpo' para salvar padronizado (só números) no SQLite
        db.cadastrar_usuario(cpf_limpo, nome, email, senha)
        flash('Conta criada com sucesso!', 'success')
        return redirect('/login')
        
    except Exception as e:
        # Se der erro no banco (como CPF ou Email já cadastrado)
        flash('Erro ao cadastrar: Este e-mail ou CPF já está em uso.', 'danger')
        return redirect('/cadastro')



# =========================
# LOGIN
# =========================
@app.route('/login', methods=['POST'])
def fazer_login():
    cpf   = request.form.get('cpf')
    senha = request.form.get('senha')
    
    usuario = db.verificar_login(cpf, senha)
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
    titulo    = request.form.get('titulo')
    categoria = request.form.get('categoria')
    descricao = request.form.get('descricao')
    latitude  = request.form.get('latitude')
    longitude = request.form.get('longitude')
    foto      = request.files.get('foto')
    anonimo   = 1 if request.form.get('anonimo') == 'on' else 0
    
    foto_caminho_salvar = os.path.join(UPLOAD_FOLDER, foto.filename)
    foto.save(foto_caminho_salvar)
    
    caminho_banco = f'static/uploads/{foto.filename}'
    
    # Salva no banco e pega o ID gerado
    protocolo = db.inserir_denuncia(titulo, categoria, descricao, latitude, longitude, caminho_banco, anonimo, sessao.get('usuario_id'))
    
    return render_template('confirmacao.html',
        protocolo=protocolo, titulo=titulo, categoria=categoria,
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
        
    db.alternar_up(denuncia_id, sessao['usuario_id'])

    # Se veio do fetch (feed), retorna JSON sem recarregar
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'ok': True})
    return redirect('/feed')


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    sessao.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)