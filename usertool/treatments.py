import os
import pandas as pd
from datetime import datetime
from . import *
from .models import PlantCost
from sqlalchemy import create_engine


class FilesTreatment:
    def __init__(self, file, commit, type):
        
        self.PRODUCTS             = ['A', 'B', 'C', 'D']
        self.PLANT_COST_COLS      = ['plant_id', 'product', 'plant_cost', 'inventory_cost', 'month_year']
        self.MAINT_CALENDAR_COLS  = ['plant_id', 'product', 'product', 'initial_time', 'final_time', 'comment']  
        self.VALID_COLS           = self.PLANT_COST_COLS if type == 'plant_cost' else self.MAINT_CALENDAR_COLS

        self.filename      = file
        self.type          = type
        self.creation_date = datetime.now().strftime('%Y-%m')
        
        self.commit = commit
        self.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    def load_raw_file(self):
        if self.filename.endswith('.csv'):
            self.df = pd.read_csv(self.filename)
        else:
            self.df = pd.read_excel(self.filename)
    
    def normalize_columns(self):
        #Normalize all columns to lower case and replace spaces with underscores and considering VALID_COLS
        self.df.columns = [col.lower().replace(' ', '_') for col in self.df.columns]
        col_mapping     = {col.lower: col for col in self.VALID_COLS}
        self.df.rename(columns=col_mapping, inplace=True)

    def clean_data(self):
        #Ensure that all columns are in VALID_COLS
        missing_cols = [col for col in self.VALID_COLS if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")
        
        # Drop rows with missing values and duplicates
        self.df.dropna(inplace=True)
        self.df.drop_duplicates(inplace=True)

        # Columns data treatment to ensure data consistency (numeric,string,date consistency)   
        self.df['plant_id']        = self.df['plant_id'].astype('str').str.strip()
        self.df['product']         = self.df['product'].astype('str').str.upper().str.strip()

        if self.type == 'plant_cost':  
            self.df['plant_cost']      = self.df['plant_cost'].astype(float)
            self.df['inventory_cost']  = self.df['inventory_cost'].astype(float)
            self.df['month_year']      = pd.to_datetime(self.df['month_year'], format='%Y-%m', errors='coerce')
        else:
            self.df['initial_time']    = pd.to_datetime(self.df['initial_time'], format='%Y-%m-%d', errors='coerce')
            self.df['final_time']      = pd.to_datetime(self.df['final_time'], format='%Y-%m-%d', errors='coerce')

        # Ensure that all products are valid
        invalid_products = self.df[~self.df['product'].isin(self.PRODUCTS)]
        if not invalid_products.empty:
            raise ValueError(f"Invalid products: {invalid_products['product'].unique()}")	 

        # Ensure that all products are valid and drop invalid products
        self.df = self.df[self.df['product'].isin(self.PRODUCTS)]

    def move_processed_file(self):
        processed_filename = f"{os.path.splitext(os.path.basename(self.filename))[0]}_{self.creation_date}{os.path.splitext(self.filename)[1]}"
        processed_path = os.path.join(
            os.path.abspath(os.path.dirname(self.filename)),
            app.config["PROCESSED_DATA"],
            processed_filename
        )
        self.df.to_excel(processed_path, index=False)

    def process_file(self):
        self.load_raw_file()
        self.normalize_columns()
        self.clean_data()

        if self.commit:
            app.logger.debug('Salvando arquivo tratado no banco de dados.')
            table = PLANT_COST if self.type == 'plant_cost' else CALENDAR
            self.df.to_sql(table, con=self.engine, if_exists='append', index=False)  
            app.logger.info(f'Arquivo salvo na tabela {SCHEMA}.{PLANT_COST}')
        return self.df    