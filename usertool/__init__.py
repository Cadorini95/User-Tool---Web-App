## IMPORTAÇÃO DE BIBLIOTECAS PARA CONFIGURAÇÃO DE APLICAÇÃO FLASK
from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
#from flask_login      import LoginManager
#from flask_bcrypt     import Bcrypt

## IMPORTAÇÃO DE BIBLIOTECAS PARA CONFIGURAÇÃO DE LOGGING
import os
import logging
from logging.handlers import RotatingFileHandler


## CONFIGURAÇÃO DE CONEXÃO COM O BANCO DE DADOS
SQL_SERVER = 'DESKTOP-SNIR42A'
DATABASE   = 'UserTool'
DRIVER     = 'ODBC Driver 17 for SQL Server'

params = urllib.parse.quote_plus(
    f"DRIVER={DRIVER};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

## CONFIGURAÇÃO DAS TABELAS DO MODELO DO BANCO DE DADOS
SCHEMA     = 'dbo'
PLANT_COST = 'PLANT_COST'
CALENDAR   = 'MAINT_CALENDAR'

## CONFIGURAÇÃO DA APLICAÇÃO FLASK
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={params}"
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

    app.logger.setLevel(logging.INFO)
    app.logger.info('UserTool startup')
