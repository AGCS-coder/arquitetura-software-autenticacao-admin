# Modelo 1 — Controle de acesso da interface administrativa

Implementação do controle de acesso da interface administrativa do exemplo construído em aula, mantendo a arquitetura base em Flask, Flask-Admin e SQLAlchemy.

## O que foi implementado

- Proteção da interface do **Flask-Admin** por autenticação.
- Tela de login em `/admin/login`.
- Redirecionamento para o login quando `/admin` é acessado sem autenticação.
- Logout em `/admin/logout`, também disponível como **Sair** no menu administrativo.
- Proteção **CSRF** no formulário de login.
- Senha armazenada somente como **hash scrypt**, nunca em texto puro.
- Usuário, hash da senha e `SECRET_KEY` configurados por variáveis de ambiente.
- `.env` incluído no `.gitignore` para evitar o envio de credenciais ao GitHub.
- `.env.example` fornecido como modelo para configuração do ambiente.

## Como executar no Windows

1. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

3. Copie `.env.example` para `.env` e preencha `SECRET_KEY` e `ADMIN_PASSWORD_HASH`.

4. Execute:

```powershell
flask --app loja/app.py:create_app run --debug
```

5. Acesse `http://127.0.0.1:5000/admin/login`.

## Gerar um novo hash de senha

O projeto usa `scrypt` para derivar o hash da senha. Execute este script Python:

```python
import base64
import hashlib
import secrets

password = input("Nova senha: ").encode("utf-8")
salt = secrets.token_bytes(16)
digest = hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1, dklen=64)

b64 = lambda value: base64.urlsafe_b64encode(value).decode().rstrip("=")
print(f"scrypt$16384$8$1${b64(salt)}${b64(digest)}")
```

Cole o resultado em `ADMIN_PASSWORD_HASH` no `.env`.

## Segurança

- O arquivo `.env` não deve ser versionado.
- A senha original não é armazenada no projeto nem no banco de dados.
- O login utiliza proteção CSRF.
- A sessão administrativa é encerrada pelo logout.

> Nunca publique o arquivo `.env` no repositório.
