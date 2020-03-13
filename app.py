#--------------------------------------
#     Author: Na Wang
#     Date: March 8, 2020
#
#--------------------------------------------
#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

#SQL query libraries
import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd
#-------------------------------------------

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://nk:nK1234@52.184.187.170:1433/test?driver=SQL+Server+Native+Client+11.0" #11.0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Initialized Marshmallow
ma = Marshmallow(app)



# Product Class/Model
class Emp(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  zip = db.Column(db.String(5))
  
# Static test
@app.route("/")
def hello():
  return "Hello Noah!"

# Employee Schema
class  EmpSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'zip')

# Init schema
emp_schema = EmpSchema()
emps_schema = EmpSchema(many=True)

# Get All Employees
@app.route('/emp', methods=['GET'])
def get_emps():
  all_emps = Emp.query.all()
  result = emps_schema.dump(all_emps)
  return jsonify(result)

	
# Get Single Employee
@app.route('/emp/<id>', methods=['GET'])
def get_emp(id):
  emp = Emp.query.get(id)
  return emp_schema.jsonify(emp)
  
# Run Server
if __name__ == '__main__':
  app.run(debug=True)

  

