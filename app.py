import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, flash, render_template
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from service import Parse_Excel
from models import *

load_dotenv()

# app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)
DATE = datetime.now()

if not os.path.isdir(os.getenv('UPLOAD_FOLDER')):
    os.mkdir(os.getenv('UPLOAD_FOLDER'))

# before request - create db
@app.before_request
def create_table():
    db.create_all()

# marshmallow
ma = Marshmallow(app)

# serialization
class ExcelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Excel_Data

# schema obj
excel_schema = ExcelSchema()
excels_schema = ExcelSchema(many=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in os.getenv('ALLOWED_EXTENSIONS')

# routing
@app.route('/')
def index():       
    return render_template('index.html')

@app.route('/data', methods = ['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        date = request.form.get('date')
        try:
            data = Excel_Data.query.filter_by(create_at=date).all()
            if data:
                return render_template('data.html', data=data)
            else:
                flash('Нет данных для загрузки')
                return render_template('data.html')
        except Exception:
            flash('Нет данных для загрузки')
            return render_template('data.html')
    return render_template('data.html')


@app.route('/upload', methods = ['POST'])
def upload_file():  
    table = {}
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не выбран файл для загрузки')
            return render_template('index.html')
        file = request.files['file']
        if file.filename == '':
            flash('Не выбран файл для загрузки')
            return render_template('index.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Parse_Excel.load_db(file)
            tables = Excel_Data.query.filter_by(create_at=DATE.strftime("%Y-%m-%d")).all()  
            table = excels_schema.dump(tables)
            return render_template('uploads.html', filename=filename, table=table)
        else:
            flash('Для загрузки разрешены только следующие форматы: xls, xlsx')
            return render_template('index.html')
    else:
        return render_template('index.html')
   
    
if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'))