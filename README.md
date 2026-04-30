# DevHub

Mini rede social feita com Django para compartilhar posts curtos, comentar, seguir usuarios e curtir publicacoes.

## Funcionalidades

- Cadastro, login e logout de usuarios.
- Feed com filtro `Todos` e `Seguindo`.
- Criacao e exclusao de posts.
- Comentarios em posts e exclusao do proprio comentario.
- Perfil publico por usuario com bio, foto e contagem de seguidores/seguindo.
- Seguir e deixar de seguir usuarios.
- Curtir e descurtir posts com contador de curtidas.
- Mensagens de feedback para acoes (sucesso/erro).

## Stack

- Python 3
- Django `5.2.x`
- SQLite (`db.sqlite3`)
- HTML + CSS (templates do Django)

## Estrutura do Projeto

```text
dev hub/
|- accounts/               # Login, cadastro e logout
|- posts/                  # Dominio principal: posts, comentarios, perfil, follow, like
|  |- templates/
|  |- static/
|  `- migrations/
|- config/                 # settings.py, urls.py, asgi.py, wsgi.py
|- media/                  # Uploads de imagem de perfil
|- manage.py
`- db.sqlite3
```

## Modelos Principais

- `Post`: autor, mensagem (ate 280), data de criacao.
- `Comment`: autor, mensagem, post relacionado, data.
- `Perfil`: usuario, bio, foto, data.
- `Follow`: relacao seguidor -> seguido.
- `Like`: usuario + post com unicidade por par (`unique_together`).

## Requisitos

Instale as dependencias pelo arquivo do projeto:

```bash
pip install -r requirements.txt
```

`Pillow` e necessario por causa do `ImageField`.

## Como Rodar Localmente

### 1) Clone o projeto

```bash
git clone <url-do-repo>
cd "dev hub"
```

### 2) Crie e ative ambiente virtual

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### 3) Instale dependencias

```bash
pip install -r requirements.txt
```

### 4) (Opcional) Configure variaveis de ambiente

Windows (PowerShell):

```powershell
$env:DJANGO_SECRET_KEY="troque-esta-chave"
$env:DJANGO_DEBUG="True"
$env:DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
```

Linux/macOS:

```bash
export DJANGO_SECRET_KEY="troque-esta-chave"
export DJANGO_DEBUG="True"
export DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
```

### 5) Aplique migracoes

```bash
python manage.py migrate
```

### 6) Execute o servidor

```bash
python manage.py runserver
```

Acesse:

- `http://127.0.0.1:8000/`

## Rotas Principais

- `/` -> pagina inicial
- `/register/` -> cadastro
- `/login/` -> login
- `/logout/` -> logout
- `/feed/` -> feed
- `/feed/create` -> criar post
- `/feed/<id>` -> detalhe do post
- `/feed/user/<username>` -> perfil
- `/feed/user/<username>/edit_profile` -> editar perfil
- `/feed/user/<username>/follow` -> seguir (`POST`)
- `/feed/user/<username>/unfollow` -> deixar de seguir (`POST`)
- `/feed/<post_id>/like` -> curtir/descurtir (`POST`)

## Seguranca e Comportamento

- Acoes que alteram estado usam `POST` e `CSRF token`.
- Views de detalhe/acao usam `get_object_or_404` para evitar erro 500 em objeto inexistente.
- Fluxo de comentario no detalhe segue padrao `POST -> redirect -> GET` (evita repost ao atualizar pagina).

## Midia e Arquivos Estaticos

- `STATIC_URL = /static/`
- `MEDIA_URL = /media/`
- `MEDIA_ROOT = BASE_DIR / "media"`
- A pasta `media/` esta no `.gitignore` (uploads locais nao sao versionados).

Durante desenvolvimento, o projeto ja esta configurado para servir `media` via `config/urls.py`.

## Status Atual

- Projeto funcional para desenvolvimento local.
- Ainda sem suite de testes automatizados implementada (`posts/tests.py` e `accounts/tests.py`).

## Proximos Passos Recomendados

1. Criar `requirements.txt` para facilitar setup.
2. Implementar testes de autenticacao e fluxo social.
3. Ajustar configuracao para producao (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` via variaveis de ambiente).
4. Padronizar URLs com barra final.

## Licenca

Defina a licenca que deseja usar (ex.: MIT).
