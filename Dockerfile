# Use uma imagem base do Python
FROM python:3.10-slim

# Instala dependências do sistema necessárias para o Poetry e configura o ambiente Python
RUN apt-get update \
    && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    unixodbc-dev \
    libodbc1 \
    odbcinst \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Copia apenas o arquivo pyproject.toml para o container
COPY pyproject.toml /app/

# Instala as dependências do projeto usando o Poetry
RUN poetry install --no-root

# Copiar o restante dos arquivos do projeto para o container
COPY . /app

# Define a variável de ambiente para o Poetry não criar um ambiente virtual
ENV FLASK_APP=main.py

# Define o ENTRYPOINT para o Poetry
ENTRYPOINT ["poetry", "run", "flask", "run"]

# Define os argumentos padrão para o Flask
CMD ["--host=0.0.0.0", "--port=8040"]