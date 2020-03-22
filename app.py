#--------------------------------------
#     Author:: Noah Kawasaki
#     Date:: March 8, 2020
#
#
#
#--------------------------------------------
#!flask/bin/python
from flask import Flask, jsonify
#from flask import abort
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

#SQL query libraries
import pyodbc
#import sqlalchemy as sal
#from sqlalchemy import create_engine
import pandas as pd
#-------------------------------------------

from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials

#----------------------------
app = Flask(__name__)


VAULT_URL = 'https://devcu-kv.vault.azure.net/' 
USR_SECRET = 'usr'
PASS_SECRET = 'passwd'
USR_SECRET_VERSION = '0bdad91564384ad0a459ad5ba5c941c5'
PASS_SECRET_VERSION = 'd7c1186833da4612bb7e2707b53306d2'

credentials = ServicePrincipalCredentials(
    client_id = '0dafa328-0f67-40cb-97bc-8b38b28931af',
    secret = 'licTySGcAk16Ly8IuK/v-1Uc?oamNBR/',
    tenant = '76b869e6-f3cf-4e3e-b85e-2a0e58ad9b63'
)

client = KeyVaultClient(credentials)

Usr = client.get_secret(VAULT_URL, USR_SECRET, USR_SECRET_VERSION ).value
Pass = client.get_secret(VAULT_URL, PASS_SECRET, PASS_SECRET_VERSION ).value


print('Username: ' +Usr +'\n Password: ' +Pass)
#app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://nk:nK1234@52.179.161.106:1433/test?driver=ODBC Driver 17 for SQL Server"#11.0

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://"+ Usr+ ":" +Pass + "@52.179.161.106:1433/test?driver=ODBC Driver 17 for SQL Server"
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
@app.route('/')
def hello():
  return 'Specify correct URL!'

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

  

