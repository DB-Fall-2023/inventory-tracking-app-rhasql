from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from handler.PartHandler import PartHandler
from handler.UserHandler import UserHandler
from handler.RacksHandler import RacksHandler
from handler.supplier import SupplierHandler
from handler.SuppliesHandler import SuppliesHandler
from handler.WarehouseHandler import WarehouseHandler
from handler.itHandler import ITHandler
from handler.otHandler import OTHandler
app = Flask(__name__)

CORS(app)

@app.route('/')
def greeting():
    return 'This is a DB test' #left for testing purposes

@app.route('/rhasql/parts', methods=['GET', 'POST'])
def getAllParts():
    if request.method == 'POST': #adds a part
        return PartHandler().addPart(request.json) #I think request.args is the solution? worked so far
    else:
        return PartHandler().getAllParts() #returns all parts
@app.route('/rhasql/parts/<int:p_id>', methods=['GET', 'PUT', 'DELETE']) #Get, Update, and Delete parts
def getPart(p_id):
    if request.method == 'GET': #returns part by id
        return PartHandler().getPart(p_id)
    elif request.method == 'PUT': #updates part by id
        return PartHandler().updatePart(p_id, request.json)
    elif request.method == 'DELETE': #deletes part by id
        return PartHandler().deletePart(p_id)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405


@app.route('/rhasql/wUser', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        return UserHandler().addUser(request.json)
    else:
        return UserHandler().getAllUsers()

@app.route('/rhasql/wUser/<int:u_id>', methods = ['GET', 'PUT', 'DELETE'])
def getUserById(u_id):
    if request.method == 'GET':
        return UserHandler().getUserById(u_id)
    elif request.method == 'PUT':
        return UserHandler().updateUser(u_id, request.json)
    elif request.method == 'DELETE':
        return UserHandler().deleteUser(u_id)
    else:
        jsonify(Error = "Method not allowed."), 405



@app.route('/rhasql/racks', methods=['GET', 'POST'])
def getAllRacks():
    if request.method == 'POST':
        return RacksHandler().insertRack(request.json)
    else:
        return RacksHandler().getAllRacks()

@app.route('/rhasql/racks/<int:r_id>', methods = ['GET', 'PUT', 'DELETE'])
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
@app.route('/rhasql/Incoming_transactions', methods = ['GET', 'POST'])
def getAllITTransactions():
    if request.method == 'POST':
        return ITHandler().insertIT(request.json)
    if request.method == 'GET':
        return ITHandler().getAllIT()
    else:
        return jsonify("Not supported"), 405
@app.route('/rhasql/Incoming_transactions/<int:it_id>', methods = ['GET', 'PUT', 'DELETE'])
def getITTransactions(it_id):
    if request.method == 'GET':
        return ITHandler().getIT(it_id)
    if request.method == 'PUT':
        return ITHandler().updateIT(it_id, request.json)
    else:
        return jsonify("Not supported"), 405

@app.route('/rhasql/Outgoing_transactions', methods = ['GET', 'POST'])
def getAllOTTransactions():
    if request.method == 'POST':
        return OTHandler().insertOT(request.json)
    if request.method == 'GET':
        return OTHandler().getAllOT()
    else:
        return jsonify("Not supported"), 405

@app.route('/rhasql/Outgoing_transactions/<int:ot_id>', methods = ['GET', 'PUT', 'DELETE'])
def getOTTransactions(ot_id):
    if request.method == 'GET':
        return OTHandler().getOT(ot_id)
    if request.method == 'PUT':
        return OTHandler().updateOT(ot_id, request.json)
    else:
        return jsonify("Not supported"), 405

@app.route('/rhasql/warehouse/<int:w_id>/rack/lowstock', methods = ['POST'])
def getLowStock(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getLowStock(w_id)
@app.route('/rhasql/warehouse/<int:w_id>/expensive', methods = ['POST'])
def getExpensiveRacks(w_id):
    if request.method == 'POST':
        return WarehouseHandler().getExpensiveRacks(w_id)
if __name__ == '__main__':
    app.run(debug=True)



