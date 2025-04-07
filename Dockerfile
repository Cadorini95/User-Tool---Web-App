# Usar a imagem oficial do Python 3.10
FROM python:3.10-slim

# Instalar dependências do sistema necessárias para o Poetry, pyodbc e o ODBC Driver 17 for SQL Server
RUN apt-get update \
    && apt-get install -y \
    curl \
    build-essential \
    # Biblioteca para suporte a SSL/TLS
    libssl-dev \
    libffi-dev \
    python3-dev \
    unixodbc \
    unixodbc-dev \
    libpq-dev \
    libsqlite3-dev \
    libodbc1 \
    odbcinst \
    odbcinst1debian2 \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# Instalar o mssql-tools e adicionar ao PATH - Testar conexão ao banco de dados via BASH
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> /etc/bash.bashrc \
    && rm -rf /var/lib/apt/lists/*

# Adicionar o diretório do sqlcmd ao PATH no ambiente do container - SQLCMD
ENV PATH="$PATH:/opt/mssql-tools/bin"

# Instalar dependências adicionais, incluindo o utilitário ping
RUN apt-get update \
    && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicionar o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Adicionar o diretório do sqlcmd ao PATH
ENV PATH="$PATH:/opt/mssql-tools/bin"

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo pyproject.toml e poetry.lock para o container
COPY pyproject.toml poetry.lock /app/
COPY usertool /app/usertool

# Instalar as dependências do projeto usando o Poetry
RUN poetry install --no-root

# Copiar o restante dos arquivos do projeto para o container
COPY main.py /app/

# Definir a variável de ambiente FLASK_APP
ENV FLASK_APP=/app/main.py

# Definir o ENTRYPOINT para rodar o Flask com o Poetry
ENTRYPOINT ["poetry", "run", "flask", "run"]

# Definir o CMD para passar os parâmetros padrão
CMD ["--host=0.0.0.0", "--port=8040"]
