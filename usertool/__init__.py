## IMPORTAÇÃO DE BIBLIOTECAS PARA CONFIGURAÇÃO DE APLICAÇÃO FLASK
from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib.parse

import os
from dotenv import load_dotenv
#from flask_login      import LoginManager
#from flask_bcrypt     import Bcrypt

## IMPORTAÇÃO DE BIBLIOTECAS PARA CONFIGURAÇÃO DE LOGGING
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy.pool import NullPool

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

## CONFIGURAÇÃO DE CONEXÃO COM O BANCO DE DADOS (USANDO VARIÁVEIS DE AMBIENTE)
SQL_SERVER = os.getenv('DB_HOST')
DATABASE   = os.getenv('DB_NAME')
USERNAME   = os.getenv('DB_USER')
PASSWORD   = os.getenv('DB_PASSWORD')
DRIVER     = 'ODBC Driver 17 for SQL Server'

params = urllib.parse.quote_plus(
    f"DRIVER={DRIVER};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)

## CONFIGURAÇÃO DAS TABELAS DO MODELO DO BANCO DE DADOS
SCHEMA     = 'dbo'
PLANT_COST = 'PLANT_COST'
CALENDAR   = 'MAINT_CALENDAR'

## CONFIGURAÇÃO DA APLICAÇÃO FLASK
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]  = f"mssql+pyodbc:///?odbc_connect={params}"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,  # Verifica se a conexão está ativa antes de usá-la
    "pool_recycle": 280,    # Recicla conexões após 280 segundos
    "pool_size": 5,         # Número máximo de conexões no pool
    "max_overflow": 10,     # Número máximo de conexões extras
    "pool_timeout": 30      # Tempo limite para obter uma conexão do pool
}
app.config["SECRET_KEY"]               = "9258d3797fb989e5b4ef270bfb9fb33c"        ## SENHA CRIPTOGRADA DE CONFIGURAÇÃO DA APLICAÇÃO
app.config["PLANT_COST_UPLOAD"]        = "static\plant_cost"                       ## CONFIGURAÇÃO DA PASTA PADRÃO PARA UPLOAD DOS ARQUIVOS DE CUSTOS DE PLANTA
app.config["MAINTENANCE_COST_UPLOAD"]  = "static\maint_calendar"                   ## CONFIGURAÇÃO DA PASTA PADRÃO PARA UPLOAD DOS ARQUIVOS DE MANUTENÇÃO DE PLANTAS
app.config["PROCESSED_DATA"]           = "static\processed_data"                   ## CONFIGURAÇÃO DA PASTA PADRÃO PARA ARMAZENAMENTO DOS ARQUIVOS PROCESSADOS  
 
database      = SQLAlchemy(app)
#bcrypt        = Bcrypt(app)
#login_manager = LoginManager(app)
#login_manager.login_view = "homepage" 

from usertool import routes


# Configuração de logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/usertool.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info(f"String de conexão gerada: {app.config['SQLALCHEMY_DATABASE_URI']}")    
    app.logger.info('UserTool startup')    
    app.logger.setLevel(logging.INFO)
    app.logger.info(f"DB_HOST: {SQL_SERVER}")    
    app.logger.info(f"DB_NAME: {DATABASE}")
    app.logger.info(f"DB_USER: {USERNAME}")
    app.logger.info(f"DB_PASSWORD: {PASSWORD}")
