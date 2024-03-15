from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


# init db
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
    db.session.append(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)


# update-put
@app.route('/employee/<id>', methods=['PUT'])
def update_product(id):
    employee = Employee.query.get(id)
    name = request.json['name']
    age = request.json['age']
    salary = request.json['salary']

    employee.name = name
    employee.price = age
    employee.salary = salary

    db.session.commit()
    return employee_schema.jsonify(employee)


# Get employee
@app.route('/employee', methods=['GET'])
def get_all_employees():
        all_employees = Employee.query.all()
        result = employees_schema.dump(all_employees)
        return jsonify(result)

# get single info using id
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    data = Employee.query.get(id)
    return employee_schema.jsonify(data)

# Delete
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'error': 'employee not found'}), 404

    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


# Initialize database
with app.app_context():
    db.create_all()

# run app
if __name__ == '__main__':
    app.run(debug=True)
