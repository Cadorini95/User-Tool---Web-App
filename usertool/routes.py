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
            path_file = os.path.join(   
                                        os.path.abspath(os.path.dirname(__file__)),  ## LOCAL ONDE ARQUIVO routes.py ESTÁ HOSPEDADO
                                        app.config["PLANT_COST_UPLOAD"], 
                                        filename
                                    )
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