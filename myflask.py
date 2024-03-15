from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# set database
# mysql database
# MYSQL_USERNAME = 'root'
# MYSQL_PASSWORD = 'Mdelisa@2'
# MYSQL_HOST = 'Local instance MYSQL80'  # or your MySQL host
# MYSQL_DB_NAME = 'MYSQL Workbench'
# # set database
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB_NAME}'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False  # complaining console # complaining console

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# Initialize database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Product class
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    salary = db.Column(db.Float)

    def __init__(self, name, age, salary):
        self.id = id
        self.name = name
        self.age = age
        self.salary = salary


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('name', 'age', 'salary')


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


@app.route('/employee', methods=['POST'])
def add_employee():
    name = request.json['name']
    age = request.json['age']
    salary = request.json['salary']

    new_employee = Employee(name, age, salary)
    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
