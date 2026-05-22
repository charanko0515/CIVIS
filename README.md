# CIVIS
**Controle Inteligente de Vigilância e Impacto Social**

Projeto desenvolvido por estudantes do **CETI Zacarias de Góis** — 4ª GRE Teresina,
para o programa **Do Piauí para o Mundo 2026**.

---

## Equipe

| Nome | Função |
|---|---|
| Maria Alice Alves Mendes | Desenvolvimento |
| Maria Clara Rodrigues da Silva | Desenvolvimento |
| José Wanderson da Silva Trindade | Desenvolvimento |
| Marcelo Augusto de Sousa Medeiros | Desenvolvimento |
| Paulo Vitor | Desenvolvimento |

---

## O que é

O CIVIS é uma plataforma web que permite a moradores de bairros periféricos registrar ocorrências urbanas (buracos, falta de iluminação, esgoto, lixo) com foto e geolocalização. As denúncias são transformadas em dados estratégicos para gestores públicos, com mapa interativo por região e número de protocolo para acompanhamento.

---

## Funcionalidades

- Registro de ocorrências com categoria, descrição, foto e localização
- 3 formas de selecionar o local: GPS automático, busca por endereço (Nominatim) ou clique no mapa
- Mapa Leaflet interativo limitado ao Brasil exibindo ocorrências do banco em tempo real
- Geração de protocolo digital após envio da denúncia
- Página de confirmação com dados da ocorrência registrada
- Cadastro e login de usuários com CPF, e-mail e senha
- Interface responsiva com herança de templates via Jinja2 (`base.html`)
- Seção informativa com curva SVG e estatísticas do projeto
- Validação no frontend bloqueando envio sem localização selecionada

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python + Flask | Backend e rotas da aplicação |
| SQLite | Banco de dados local |
| Jinja2 | Templates HTML com herança (`base.html`) |
| Tailwind CSS | Estilização via CDN |
| Leaflet.js | Mapa interativo |
| OpenStreetMap | Tiles do mapa (gratuito, sem chave de API) |
| Nominatim API | Busca de endereços por texto |
| Font Awesome 6 | Ícones da interface |
| Plus Jakarta Sans | Tipografia principal (Google Fonts) |

---

## Estrutura do projeto

```
CIVIS/
├── app.py                  # Rotas Flask
├── database.py             # Criação das tabelas SQLite
├── database.db             # Banco de dados gerado
├── static/
│   ├── prototiple.png      # Imagem de referência do protótipo
│   └── uploads/            # Fotos enviadas pelos usuários
└── templates/
    ├── base.html           # Template base (header, breadcrumb, footer)
    ├── homepage.html       # Formulário de denúncia + mapa + seção informativa
    ├── login.html          # Página de login por CPF e senha
    ├── cadastro.html       # Página de cadastro de usuário
    └── confirmacao.html    # Confirmação com número de protocolo
```

---

## Banco de dados

**Tabela `denuncias`**

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Protocolo gerado automaticamente |
| categoria | TEXT NOT NULL | Tipo de ocorrência |
| latitude | REAL NOT NULL | Coordenada geográfica |
| longitude | REAL NOT NULL | Coordenada geográfica |
| foto_caminho | TEXT NOT NULL | Caminho do arquivo salvo |
| descriacao | TEXT NOT NULL | Descrição da ocorrência |
| data_registro | DATETIME | Data/hora do registro (automática) |

**Tabela `usuario`**

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| cpf | TEXT UNIQUE NOT NULL | CPF único do usuário |
| name | TEXT NOT NULL | Nome completo |
| email | TEXT UNIQUE NOT NULL | E-mail único |
| password | TEXT NOT NULL | Senha |
| data_criação | DATETIME | Data de cadastro (automática) |

---

## Rotas do app.py

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Homepage com formulário e mapa |
| GET | `/login` | Página de login |
| POST | `/login` | Valida CPF e senha, redireciona |
| GET | `/cadastro` | Página de cadastro |
| POST | `/cadastro` | Insere novo usuário no banco |
| POST | `/receber_denuncia` | Salva foto + denúncia e abre confirmação |

---

## Como rodar

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/civis.git
cd civis
```

**2. Instale as dependências**
```bash
pip install flask
```

**3. Crie o banco de dados**
```bash
python database.py
```

**4. Inicie o servidor**
```bash
python app.py
```

**5. Acesse no navegador**
```
http://localhost:5000
```

---

## Observações importantes

- O GPS só funciona em `localhost` ou em conexões **HTTPS**. Para testar no celular na rede local, use o [ngrok](https://ngrok.com):
```bash
ngrok http 5000
```
- As fotos enviadas são salvas em `static/uploads/`
- O banco `database.db` é criado automaticamente ao rodar `database.py`
- Para reiniciar o banco do zero, delete o `database.db` e rode `database.py` novamente
- O VS Code pode sublinhar `{{ ocorrencias | tojson | safe }}` como erro de sintaxe — isso é normal, o Jinja2 processa corretamente em tempo de execução

---

## Fluxo de uso

```
Usuário acessa /
        ↓
Seleciona categoria, endereço (GPS / busca / clique no mapa), descrição e foto
        ↓
Valida localização no frontend (bloqueia envio se vazia)
        ↓
POST /receber_denuncia → salva foto em static/uploads/ + insere no banco
        ↓
Página confirmacao.html com número do protocolo, categoria, coordenadas e data
```

---

## Histórico de melhorias (sessão atual)

- Criação do `base.html` com herança Jinja2 eliminando repetição entre páginas
- Adição do mapa Leaflet com tiles OpenStreetMap dentro de mockup de celular
- Implementação de 3 formas de seleção de localização (GPS, busca, clique)
- Limitação do mapa ao território brasileiro com `maxBounds`
- Barra de busca com ícone interno (padrão `search-wrap`)
- Ocorrências do mapa carregadas dinamicamente do banco de dados
- Página de confirmação com protocolo gerado pelo `lastrowid`
- Validação frontend impedindo envio sem localização
- Seção informativa com curvas SVG e estatísticas abaixo do hero
- Campo `descriacao` adicionado ao formulário e ao banco

---

*CIVIS · CETI Zacarias de Góis · Do Piauí para o Mundo 2026*