from flask import Flask, jsonify, request, render_template, make_response
from flask_cors import CORS
from handler.PartHandler import PartHandler
from handler.UserHandler import UserHandler
from handler.RacksHandler import RacksHandler
from handler.supplier import SupplierHandler
from handler.SuppliesHandler import SuppliesHandler
from handler.WarehouseHandler import WarehouseHandler
from handler.itHandler import ITHandler
from handler.otHandler import OTHandler
from handler.exchangeHandler import ExchangeHandler
from subprocess import Popen
import os
import subprocess
import time

app = Flask(__name__)

CORS(app)

@app.route('/')
def greeting():
    return 'This is a DB test' #left for testing purposes

@app.route('/rhasql/part', methods=['GET', 'POST'])
def getAllParts():
    if request.method == 'POST': #adds a part
        return PartHandler().addPart(request.json) #I think request.args is the solution? worked so far
    elif request.method == 'GET':
        return PartHandler().getAllParts() #returns all parts
    else:
        return jsonify(Error="Method not allowed."), 405
@app.route('/rhasql/part/<int:p_id>', methods=['GET', 'PUT', 'DELETE']) #Get, Update, and Delete parts
def getPart(p_id):
    if request.method == 'GET': #returns part by id
        return PartHandler().getPart(p_id)
    elif request.method == 'PUT': #updates part by id
        return PartHandler().updatePart(p_id, request.json)
    elif request.method == 'DELETE': #deletes part by id
        return PartHandler().deletePart(p_id)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405


@app.route('/rhasql/user', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        return UserHandler().addUser(request.json)
    elif request.method == 'GET':
        return UserHandler().getAllUsers()
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/user/<int:u_id>', methods = ['GET', 'PUT', 'DELETE'])
def getUserById(u_id):
    if request.method == 'GET':
        return UserHandler().getUserById(u_id)
    elif request.method == 'PUT':
        return UserHandler().updateUser(u_id, request.json)
    elif request.method == 'DELETE':
        return UserHandler().deleteUser(u_id)
    else:
        jsonify(Error = "Method not allowed."), 405



@app.route('/rhasql/rack', methods=['GET', 'POST'])
def getAllRacks():
    if request.method == 'POST':
        return RacksHandler().insertRack(request.json)
    elif request.method == 'GET':
        return RacksHandler().getAllRacks()
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/rack/<int:r_id>', methods = ['GET', 'PUT', 'DELETE'])
def getRacksById(r_id):
    if request.method == 'GET':
        return RacksHandler().getRacksById(r_id)
    elif request.method == 'PUT':
        return RacksHandler().updateRack(r_id, request.json)
    elif request.method == 'DELETE':
        return RacksHandler().deleteRack(r_id)
    else:
        jsonify(Error = "Method is not allowed."), 405

#Routes for Supplier table
@app.route('/rhasql/supplier', methods=['GET', 'POST'])
def getAllSuppliers():
    if request.method == 'GET':
        return SupplierHandler().getAllSuppliers()

    elif request.method == 'POST':
        data = request.json
        return SupplierHandler().insertSupplier(data)

    else:
        return jsonify("Not supported"), 405


@app.route('/rhasql/supplier/<int:s_id>', methods=['GET', 'PUT', 'DELETE'])
def searchSupplierById(s_id):
    if request.method == 'GET':
        return SupplierHandler().searchById(s_id)
    elif request.method == 'DELETE':
        return SupplierHandler().deleteById(s_id)
    elif request.method == 'PUT':
        data = request.json
        return SupplierHandler().updateById(s_id, data)
    else:
        return jsonify("Not supported"), 405
@app.route('/rhasql/supplies', methods=['GET','POST'])
def getAllSupplies():
    if request.method == 'POST':
        return SuppliesHandler().addSupplies(request.json)
    elif request.method == 'GET':
        return SuppliesHandler().getAllSupplies()
    else:
        return jsonify("Not supported"), 405
@app.route('/rhasql/supplies/<int:p_id>,<int:s_id>',methods=['GET','PUT', 'DELETE'])
def getSupplies(p_id,s_id):
    if request.method == 'GET':
        return SuppliesHandler().getSupplies(p_id,s_id)
    if request.method == 'PUT':
        return SuppliesHandler().updateSupplies(p_id,s_id, request.json)
    if request.method == 'DELETE':
        return SuppliesHandler().deleteSupplies(p_id,s_id)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/warehouse', methods=['GET', 'POST'])
def getAllWarehouses():
    if request.method == 'POST':
        return WarehouseHandler().insertWarehouse(request.json)
    elif request.method == 'GET':
        return WarehouseHandler().getAllWarehouses()
    else:
        return jsonify("Not supported"), 405

@app.route('/rhasql/warehouse/<int:w_id>', methods = ['GET', 'PUT', 'DELETE'])
def getWarehouseById(w_id):
    if request.method == 'GET':
        return WarehouseHandler().getWarehouseById(w_id)
    elif request.method == 'PUT':
        return WarehouseHandler().updateWarehouseById(w_id, request.json)
    elif request.method == 'DELETE':
        return WarehouseHandler().deleteByWarehouseId(w_id)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405
@app.route('/rhasql/incoming', methods = ['GET', 'POST'])
def getAllITTransactions():
    if request.method == 'POST':
        return ITHandler().insertIT(request.json)
    if request.method == 'GET':
        return ITHandler().getAllIT()
    else:  # catches any other methods
        return jsonify(Error="Method not allowed."), 405
@app.route('/rhasql/incoming/<int:it_id>', methods = ['GET', 'PUT', 'DELETE'])
def getITTransactions(it_id):
    if request.method == 'GET':
        return ITHandler().getIT(it_id)
    if request.method == 'PUT':
        return ITHandler().updateIT(it_id, request.json)
    else:  # catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/outgoing', methods = ['GET', 'POST'])
def getAllOTTransactions():
    if request.method == 'POST':
        return OTHandler().insertOT(request.json)
    if request.method == 'GET':
        return OTHandler().getAllOT()
    else:  # catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/outgoing/<int:ot_id>', methods = ['GET', 'PUT', 'DELETE'])
def getOTTransactions(ot_id):
    if request.method == 'GET':
        return OTHandler().getOT(ot_id)
    if request.method == 'PUT':
        return OTHandler().updateOT(ot_id, request.json)
    else:  # catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/exchange', methods = ['GET', 'POST'])
def getAllExchange():
    if request.method == 'POST':
        return ExchangeHandler().insertExchange(request.json)
    if request.method == 'GET':
        return ExchangeHandler().getAllExchange()
    else:  # catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/exchange/<int:ex_id>', methods = ['GET', 'PUT', 'DELETE'])
def getExchangeById(ex_id):
    if request.method == 'GET':
        return ExchangeHandler().getExchangeById(ex_id)
    if request.method == 'PUT':
        return ExchangeHandler().updateExchange(ex_id, request.json)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/warehouse/<int:w_id>/profit', methods = ['POST'])
def getProfit(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getProfit(w_id, request.json)
    else:  # catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/warehouse/<int:w_id>/rack/lowstock', methods = ['POST'])
def getLowStock(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getLowStock(w_id, request.json)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405
@app.route('/rhasql/warehouse/<int:w_id>/rack/expensive', methods = ['POST'])
def getExpensiveRacks(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getExpensiveRacks(w_id, request.json)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405
@app.route('/rhasql/warehouse/<int:w_id>/rack/material', methods = ['POST'])
def getBottomParts(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getBottomParts(w_id, request.json)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405
@app.route('/rhasql/warehouse/<int:w_id>/transaction/suppliers', methods = ['POST'])
def getMostSuppliers(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getMostSuppliers(w_id, request.json)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/warehouse/<int:w_id>/transaction/leastcost', methods = ['POST'])
def getLeastTransactions(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getLeastTransactions(w_id, request.json)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/warehouse/<int:w_id>/users/receivesmost', methods = ['POST'])
def getReceivesMost(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getReceivesMost(w_id, request.json)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/most/transactions', methods = ['GET'])
def getMostUserTransactions():
    if request.method == 'GET':
        Popen(['voila', 'JupyterNotebooks/mostUserTransactions.ipynb'])
        return UserHandler().getMostUserTransactions()
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/least/outgoing', methods = ['GET'])
def getLeastOutgoing():
    if request.method == 'GET':
        Popen(['voila', 'JupyterNotebooks/leastOutgoing.ipynb'])
        return WarehouseHandler().getLeastOutgoing()
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405


@app.route('/rhasql/most/incoming', methods=['GET'])
def getMostIncoming():
    if request.method == 'GET':
        Popen(['voila', 'JupyterNotebooks/mostIncoming.ipynb'])
        return WarehouseHandler().getMostIncoming()
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405

@app.route('/rhasql/most/city', methods=['GET'])
def getMostCities():
    if request.method == 'GET':
        Popen(['voila', 'JupyterNotebooks/mostCity.ipynb'])
        return WarehouseHandler().getMostCities()
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405
@app.route('/rhasql/most/deliver', methods=['GET'])
def getMostDeliver():
    if request.method == 'GET':
        Popen(['voila', 'JupyterNotebooks/mostDELIVER.ipynb'])
        return WarehouseHandler().getMostDeliver()
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405
@app.route('/rhasql/most/rack', methods=['GET'])
def getMostRacks():
    if request.method == 'GET':
        Popen(['voila', 'JupyterNotebooks/mostRack.ipynb'])
        return WarehouseHandler().getMostRacks()
    else: #catches any other methods
        return jsonify(Error="Method not allowed"), 405

@app.route('/rhasql/partPrice', methods=['GET'])
def getAllPrice():
     if request.method == 'GET':
         #Popen(['voila', '--port=8862','--no-browser','JupyterNotebooks/partPrice.ipynb'])

         #command = ['voila', '--port=8862', '--no-browser', 'JupyterNotebooks/partPrice.ipynb', '--Voila.tornado_settings={"headers": {"Content-Security-Policy": "frame-ancestors *"}}']
         #Popen(command)
         #print(Popen(command))
         heroku_app_url = f"https://{os.environ['HEROKU_APP_NAME']}.herokuapp.com"
         voila_url = f"{heroku_app_url}:8866/"
         return render_template('test.html', voila_url=voila_url)
#     else: #catches any other methods
#         return jsonify(Error="Method not allowed"), 405

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



