# CIVIS
**Controle Inteligente de Vigilância e Impacto Social**

Projeto desenvolvido por estudantes do **CETI Zacarias de Góis** — 4ª GRE Teresina,
para o programa **Do Piauí para o Mundo 2026**.

---

## Equipe

| Nome | Função |
|---|---|
| Marcelo Augusto de Sousa Medeiros | Desenvolvimento |
| Maria Alice Alves Mendes | Desenvolvimento |
| Maria Clara Rodrigues da Silva | Desenvolvimento |
| José Wanderson da Silva Trindade | Desenvolvimento |
| Paulo Vitor Barros de Souza | Desenvolvimento |
| Manoel Araujo Veloso Neto | Professor orientador |

---

## O que é

O CIVIS é uma plataforma web que conecta cidadãos e gestores públicos. Moradores de bairros periféricos podem registrar ocorrências urbanas com foto e geolocalização, de forma anônima ou identificada. As denúncias viram dados estratégicos para a gestão pública, com mapa interativo, número de protocolo e sistema de ups para priorização por impacto social.

---

## Funcionalidades

- Landing page com apresentação do projeto e metas esperadas
- Denúncia anônima sem necessidade de cadastro
- Registro de ocorrências com título, categoria, descrição, foto e localização
- Opção de envio anônimo ou identificado
- Preview de fotos antes do envio
- 3 formas de selecionar o local: GPS, busca por endereço ou clique no mapa
- Mapa Leaflet interativo limitado ao Brasil
- Geração de protocolo com status "Aberta" após envio
- Cadastro e login de usuários com CPF e senha
- Feed com saudação ao usuário, rolagem vertical e imagens estilo Instagram
- Sistema de ups com toggle sem recarregar a página (fetch assíncrono)
- Perfil com dados do usuário e histórico de denúncias próprias
- Menu hambúrguer com sidebar em todas as telas
- Header fixo (sticky) que acompanha o scroll
- Botão flutuante "Nova denúncia" que se adapta ao scroll
- Migrações automáticas no banco sem perda de dados

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Backend, rotas e templates | Python + Flask + Jinja2 |
| Banco de dados | SQLite |
| Estilização e ícones | Tailwind CSS + Font Awesome |
| Mapa interativo e geolocalização | Leaflet + OpenStreetMap |

---

## Estrutura do projeto

```
CIVIS/
├── app.py                  # Rotas Flask
├── adm_db.py               # Funções do banco de dados
├── database.py             # Criação e migração das tabelas
├── static/
│   ├── icons/              # Ícones do upload de foto
│   └── uploads/            # Fotos enviadas pelos usuários
└── templates/
    ├── base.html           # Template base (header, sidebar, footer)
    ├── landing.html        # Página inicial com apresentação do projeto
    ├── denuncia.html       # Formulário de denúncia + mapa
    ├── feed.html           # Feed de ocorrências com ups
    ├── perfil.html         # Perfil e histórico do usuário
    ├── login.html          # Login por CPF e senha
    ├── cadastro.html       # Cadastro de usuário
    └── confirmacao.html    # Confirmação com número de protocolo
```

---

## Banco de dados

**Tabela `usuario`**

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| cpf | TEXT UNIQUE NOT NULL | CPF único (somente dígitos) |
| nome | TEXT NOT NULL | Nome completo |
| email | TEXT NOT NULL | E-mail |
| senha | TEXT NOT NULL | Senha |
| data_criacao | DATETIME | Data de cadastro (automática) |

**Tabela `denuncias`**

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Protocolo gerado automaticamente |
| titulo | TEXT NOT NULL | Título da ocorrência |
| categoria | TEXT NOT NULL | Tipo de ocorrência |
| descricao | TEXT | Descrição detalhada |
| latitude | TEXT | Coordenada geográfica |
| longitude | TEXT | Coordenada geográfica |
| foto_caminho | TEXT | Caminho do arquivo salvo |
| anonimo | INTEGER | 1 = anônimo, 0 = identificado |
| status | TEXT | Status da denúncia (padrão: "Aberta") |
| usuario_id | INTEGER | Referência ao usuário (nullable) |
| data_registro | DATETIME | Data/hora do registro (automática) |

**Tabela `ups`**

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| denuncia_id | INTEGER NOT NULL | Referência à denúncia |
| usuario_id | INTEGER NOT NULL | Referência ao usuário |
| data_up | DATETIME | Data/hora do up (automática) |

---

```
```
                ┌──────────────────────┐
                │       usuario        │
                ├──────────────────────┤
                │ PK id                │
                │ cpf                  │
                │ nome                 │
                │ email                │
                │ senha                │
                │ data_criacao         │
                └─────────┬────────────┘
                          │ 1
                          │
                          │
                          │ N
            ┌─────────────▼─────────────┐
            │         denuncias         │
            ├───────────────────────────┤
            │ PK id                     │
            │ titulo                    │
            │ categoria                 │
            │ descricao                 │
            │ latitude                  │
            │ longitude                 │
            │ foto_caminho              │
            │ anonimo                   │
            │ status                    │
            │ data_registro             │
            │ FK usuario_id             │
            └─────────────┬─────────────┘
                          │ 1
                          │
                          │
                          │ N
                 ┌────────▼────────┐
                 │       ups       │
                 ├─────────────────┤
                 │ PK id           │
                 │ FK denuncia_id  │
                 │ FK usuario_id   │
                 │ data_up         │
                 └────────┬────────┘
                          │
                          │ N
                          │
                          │ 1
                ┌─────────▼──────────┐
                │      usuario       │
                └────────────────────┘
```

RELACIONAMENTOS:

1. usuario → denuncias

   * Um usuário pode criar várias denúncias.
   * Uma denúncia pertence a apenas um usuário.

2. denuncias → ups

   * Uma denúncia pode receber vários ups.
   * Um up pertence a apenas uma denúncia.

3. usuario → ups

   * Um usuário pode dar vários ups.
   * Cada up pertence a apenas um usuário.

```

## Rotas do app.py

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Landing page |
| GET | `/denuncia` | Formulário de denúncia |
| GET | `/feed` | Feed de ocorrências (requer login) |
| GET | `/perfil` | Perfil do usuário (requer login) |
| GET | `/login` | Página de login |
| POST | `/login` | Valida CPF e senha, redireciona para feed |
| GET | `/cadastro` | Página de cadastro |
| POST | `/cadastro` | Insere novo usuário no banco |
| POST | `/receber_denuncia` | Salva denúncia e abre confirmação |
| POST | `/up/<id>` | Toggle de up (retorna JSON sem recarregar) |
| GET | `/logout` | Encerra sessão e redireciona para `/` |

---

## Como rodar

**1. Clone o repositório**
```bash
git clone https://github.com/charanko0515/civis.git
cd civis
```

**2. Instale as dependências**
```bash
pip install flask
```

**3. Crie/atualize o banco de dados**
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

## Observações

- O GPS só funciona em `localhost` ou **HTTPS**. Para testar no celular: `ngrok http 5000`
- Fotos salvas em `static/uploads/`
- `database.py` faz migrações automáticas — não apaga dados ao rodar novamente
- Feed e perfil são protegidos — redirecionam para `/login` se não autenticado
- Up no feed usa `fetch` assíncrono — sem recarregamento de página

---

## Pontos de melhoria futura

Itens identificados para evolução do projeto:

**Segurança**
- As senhas estão armazenadas em texto puro — recomenda-se usar hash com `werkzeug.security` (`generate_password_hash` / `check_password_hash`)
- A `secret_key` está hardcoded no `app.py` — em produção, deve vir de variável de ambiente
- O nome do arquivo de foto enviado pelo usuário é salvo sem sanitização — usar `werkzeug.utils.secure_filename`

**Robustez**
- O banco é acessado com caminho relativo (`database.db`) — usar `os.path` para garantir o caminho absoluto

**Funcionalidade**
- Denúncias marcadas como anônimas ainda expõem o nome do usuário no feed — o template `feed.html` precisa verificar o campo `anonimo` antes de exibir
- A tabela `ups` não tem constraint `UNIQUE(denuncia_id, usuario_id)` — adicionar garante integridade mesmo em casos de requisições simultâneas

---

*CIVIS · CETI Zacarias de Góis · Do Piauí para o Mundo 2026*
