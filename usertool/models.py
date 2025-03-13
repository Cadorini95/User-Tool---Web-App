from datetime import datetime
from . import database as db

class Plant(db.Model):
    plant_id = db.Column(db.String(10), primary_key=True)
    plant_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)

class MaintCalendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.String(10), nullable=False)
    plant_name = db.Column(db.String(100), nullable=False)
    product = db.Column(db.String(10), nullable=False)
    initial_time = db.Column(db.DateTime, nullable=False)
    final_time = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String, nullable=True)

class PlantCost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.String(10), nullable=False)
    product = db.Column(db.String(10), nullable=False)
    plant_cost = db.Column(db.Float, nullable=False)
    inventory_cost = db.Column(db.Float, nullable=False)
    month_year = db.Column(db.DateTime, nullable=False)