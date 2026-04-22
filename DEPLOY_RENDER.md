# 📱 Guia de Deploy - Training Agent Bot no Render

Esse guia vai te levar passo a passo para colocar seu bot Telegram no Render (hospedagem grátis).

---

## 📋 Pré-requisitos

- ✅ Conta no GitHub (com seu projeto lá)
- ✅ Conta do Render (grátis em https://render.com)
- ✅ Token do seu bot Telegram (já tem em `bot_service.py`)

---

## 1️⃣ Preparar o Projeto Localmente

### 1.1 - Criar arquivo `.env`

Crie um arquivo `.env` na raiz do seu projeto com as variáveis de ambiente:

```env
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/training_agent
TELEGRAM_BOT_TOKEN=8697158652:AAHnOLuZ-Nw2nEsaRL4itHOvTcbzg_nPnU8
```

> **⚠️ IMPORTANTE:** Esse arquivo `.env` é local só. No Render você vai configurar via dashboard.

### 1.2 - Criar arquivo `.gitignore`

Crie um arquivo `.gitignore` para não subir arquivos sensíveis:

```
.env
venv/
__pycache__/
*.pyc
.DS_Store
instance/
.vscode/
.idea/
```

### 1.3 - Criar arquivo `Procfile`

Na raiz do projeto, crie um arquivo chamado `Procfile` (sem extensão):

```
worker: python app/bot_service.py
```

Isso diz ao Render para rodar o bot.

### 1.4 - Atualizar `requirements.txt`

Verifique se está assim (ou rode `pip freeze > requirements.txt`):

```
Flask
psycopg2-binary
flask-sqlalchemy
python-dotenv
pyTelegramBotAPI
```

---

## 2️⃣ Subir o Código no GitHub

```bash
cd /Users/leonardo.ogata/Documents/training-agent

# Inicializar repositório Git (se ainda não tiver)
git init

# Adicionar tudo
git add .

# Fazer primeiro commit
git commit -m "Initial commit: training agent bot"

# Adicionar remote do GitHub (substitua seu_usuario/seu_repo)
git remote add origin https://github.com/seu_usuario/training-agent.git

# Fazer push
git branch -M main
git push -u origin main
```

---

## ⚠️ Por que usar Webhooks no Render?

O plano **Free** do Render coloca o serviço para "dormir" após 15 minutos de inatividade. 
- **Antes (Polling):** O bot não recebia mensagens enquanto dormia, pois o Telegram não "acordava" o servidor.
- **Agora (Webhooks):** O bot está configurado para usar Webhooks no Render. Sempre que você envia uma mensagem, o Telegram faz uma requisição HTTP para o seu servidor, o que **acorda o serviço automaticamente**.

---

## 3️⃣ Criar PostgreSQL no Render

1. **Acesse https://render.com** e faça login
2. **Clique em "New +"** → **PostgreSQL**
3. **Preencha os dados:**
   - Name: `training-agent-db`
   - Database: `training_agent`
   - User: `postgres_user`
   - Region: Escolha a mais próxima
   - PostgreSQL Version: 15
   - Tier: **Free** (para começar)

4. **Clique em "Create Database"**
5. **Espere criar** (vai demorar alguns segundos)
6. **Copie a URL de conexão** que vai aparecer (vai ser algo como):
   ```
   postgresql://postgres_user:senha_aleatoria@seu_host.render.com:5432/training_agent
   ```

---

## 4️⃣ Deploy da Aplicação Flask + Bot

1. **Clique em "New +"** → **Web Service**

2. **Conecte seu GitHub:**
   - Clique em "Connect a repository"
   - Autorize o Render
   - Selecione `seu_usuario/training-agent`

3. **Preencha os dados:**
   - **Name:** `training-agent-bot`
   - **Region:** Mesma do banco
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`

4. **Clique em "Advanced"** e configure as variáveis de ambiente:
   - Clique em **"Add Environment Variable"**
   - Adicione:
     ```
     DATABASE_URL = (copie a URL completa do banco PostgreSQL)
     TELEGRAM_BOT_TOKEN = (seu token do bot)
     RENDER_EXTERNAL_URL = (a URL do seu app, ex: https://seu-app.onrender.com)
     FLASK_ENV = production
     ```

5. **Clique em "Create Web Service"**

6. **Espere o deploy** (pode levar 2-3 minutos)

---

## 5️⃣ Verificar se Funcionou

### Opção A: Ver os logs

1. No dashboard do Render, clique no seu serviço `training-agent-bot`
2. Vá em **"Logs"** (no menu superior)
3. Procure por mensagens como:
   ```
   Starting bot polling...
   ```

### Opção B: Testar o bot no Telegram

1. Abra o Telegram
2. Procure pelo seu bot
3. Mande `/start`
4. Se receber a lista de treinos, **funcionou! 🎉**

---

## 6️⃣ Troubleshooting

### ❌ "Bot não responde"

1. Verifique se o `TELEGRAM_BOT_TOKEN` está correto no Render
2. Cheque os logs em **Logs** → procure por erros
3. Certifique-se que o banco de dados está conectando (rode uma query de teste)

### ❌ "Erro de banco de dados"

1. Copie a `DATABASE_URL` do banco PostgreSQL
2. Vá em Settings do serviço Web
3. Procure por **"Environment"** e atualize a `DATABASE_URL`

### ❌ "Erro 500 ou similar"

1. Vá em **"Logs"**
2. Leia a mensagem de erro completa
3. Procure a linha com `ERROR` ou `Exception`

---

## 7️⃣ Updates Futuros

Sempre que você fizer mudanças:

```bash
git add .
git commit -m "Sua mensagem aqui"
git push origin main
```

O Render **automaticamente detecta** e **faz redeploy** em alguns segundos!

---

## 📊 Plano Free do Render

- ✅ PostgreSQL: Até 1GB de dados
- ✅ Web Service: Até 750 horas/mês (24/7)
- ✅ **Inatividade:** O serviço dorme após 15 min, mas **acorda sozinho** assim que você mandar qualquer mensagem para o bot no Telegram (graças ao Webhook)!
- 💰 Upgrade: A partir de $7/mês para serviço sempre ativo

---

## 🔧 Como Funciona (Technically Speaking)

O `run.py` faz o seguinte:

```python
# 1. Cria uma thread separada para o bot
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

# 2. Inicia o servidor Flask na porta 5000
app.run(host='0.0.0.0', port=port)
```

**Resultado:**
- ✅ Bot roda 24/7 em background (thread separada)
- ✅ Flask fica escutando na porta 5000 (mantém Render vivo)
- ✅ Sem custo adicional!

---

## 🎯 Próximos Passos (Opcional)

- [ ] Configurar backup automático do banco
- [ ] Adicionar logging mais detalhado
- [ ] Criar mais rotas Flask para gerenciar treinos via web
- [ ] Adicionar autenticação para APIs

---

**Dúvidas?** Cheque a documentação oficial:
- Render: https://docs.render.com
- pyTelegramBotAPI: https://github.com/eternnoir/pyTelegramBotAPI
