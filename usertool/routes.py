import os 
import pandas as pd

from flask import render_template, url_for, flash, redirect
from werkzeug.utils import secure_filename
from . import app, database
from .forms import UpdatePlantCostForm, UpdateMaintCalendarForm  
from .treatments import FilesTreatment

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/update_plant_cost', methods=['GET', 'POST'])
def update_plant_cost():
    form =  UpdatePlantCostForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            app.logger.debug('Arquivo de custo de planta enviado com sucesso!')
            filename = secure_filename(file.filename)
            
            # Garantir que o diretório exista
            upload_folder = os.path.join(app.root_path, app.config["PLANT_COST_UPLOAD"])
            os.makedirs(upload_folder, exist_ok=True)
            
            path_file = os.path.join(upload_folder, filename)
            file.save(path_file)
            app.logger.debug('Arquivo de custo de planta atualizado com sucesso') 

            plant_cost =  FilesTreatment(path_file, commit=True, type='plant_cost')

            try:
                app.logger.debug('Realizando tratamentos do arquivo enviado.')
                plant_cost.process_file()
                app.logger.info('Finalizado.')
            except ValueError as e:
                app.logger.error('Falha ao realizar tratamentos do arquivo enviado.')
                app.logger.error(e)

            return redirect(url_for('home'))
        else:
            flash('Arquivo de custo de planta não enviado. Formato inválido!', 'danger')
    return render_template('update_plant_cost.html', form=form)


@app.route('/update_maint_calendar', methods=['GET', 'POST'])
def update_maint_calendar():
    form =  UpdateMaintCalendarForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            app.logger.debug('Arquivo de calendário de manutenção enviado com sucesso!')
            filename = secure_filename(file.filename)
            path_file = os.path.join(   
                                        os.path.abspath(os.path.dirname(__file__)),  ## LOCAL ONDE ARQUIVO routes.py ESTÁ HOSPEDADO
                                        app.config["MAINTENANCE_COST_UPLOAD"], 
                                        filename
                                    )
            file.save(path_file)
            app.logger.info('Arquivo de calendário de manutenção atualizado com sucesso')

            maint_calendar =  FilesTreatment(path_file, commit=True, type='maint_calendar')

            try:
                app.logger.debug('Realizando tratamentos do arquivo enviado.')
                maint_calendar.process_file()
                app.logger.info('Finalizado.')
            except ValueError as e:
                app.logger.error('Falha ao realizar tratamentos do arquivo enviado.')
                app.logger.error(e) 

            return redirect(url_for('home'))
        else:
            flash('Arquivo de calendário de manutenção não enviado. Formato inválido!', 'danger')
    return render_template('update_maint_calendar.html', form=form)

@app.route('/test_connection_direct', methods=['GET'])
def test_connection_direct():
    import pyodbc
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={os.getenv('DB_HOST')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
            "Connection Timeout=300;"
        )
        app.logger.info(f"String de conexão direta: {conn_str}")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 10 * FROM dbo.PLANT_COST")
        rows = cursor.fetchall()
        conn.close()
        return {"status": "success", "data": [dict(zip([column[0] for column in cursor.description], row)) for row in rows]}, 200
    except Exception as e:
        app.logger.error(f"Erro ao conectar diretamente ao banco de dados: {e}")
        return {"status": "error", "message": str(e)}, 500