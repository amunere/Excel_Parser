from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class Excel_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    fact_oliq_d1 = db.Column(db.Numeric, nullable=False)
    fact_oliq_d2 = db.Column(db.Numeric, nullable=False)
    fact_ooil_d1 = db.Column(db.Numeric, nullable=False)
    fact_ooil_d2 = db.Column(db.Numeric, nullable=False)
    forecast_oliq_d1 = db.Column(db.Numeric, nullable=False)
    forecast_oliq_d2 = db.Column(db.Numeric, nullable=False)
    forecast_ooil_d1 = db.Column(db.Numeric, nullable=False)
    forecast_ooil_d2 = db.Column(db.Numeric, nullable=False)
    create_at = db.Column(db.Date, server_default=func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, company, fact_oliq_d1, fact_oliq_d2, fact_ooil_d1, fact_ooil_d2, forecast_oliq_d1, forecast_oliq_d2, forecast_ooil_d1, forecast_ooil_d2):
        self.company = company
        self.fact_oliq_d1 = fact_oliq_d1
        self.fact_oliq_d2 = fact_oliq_d2
        self.fact_ooil_d1 = fact_ooil_d1
        self.fact_ooil_d2 = fact_ooil_d2
        self.forecast_oliq_d1 = forecast_oliq_d1
        self.forecast_oliq_d2 = forecast_oliq_d2
        self.forecast_ooil_d1 = forecast_ooil_d1
        self.forecast_ooil_d2 = forecast_ooil_d2

    def __repr__(self):
        return f'<Company: {self.company}, Fact_Oliq_Data1: {self.fact_oliq_d1}, Fact_Oliq_Data1: {self.fact_oliq_d2}, Fact_Ooil_Data1: {self.fact_ooil_d1}, Fact_Ooil_Data2: {self.fact_ooil_d2}, Forecast_Oliq_Data1: {self.forecast_oliq_d1}, Fact_Oliq_Data2: {self.forecast_oliq_d2}, Forecast_Ooil_Data1: {self.forecast_ooil_d1}, Forecast_Ooil_Data2: {self.forecast_ooil_d2}>'

