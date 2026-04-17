from app import create_app

# 1. Cria a instância do aplicativo Flask
app = create_app()

if __name__ == "__main__":
    # 2. Roda o servidor de desenvolvimento
    # O debug=True permite que o Flask reinicie sozinho quando você altera o código
    app.run(debug=True)