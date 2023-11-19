from flask import jsonify
from DAO.warehouseDAO import warehouseDAO
from handler.RacksHandler import RacksHandler
from DAO.userDAO import UserDAO

class WarehouseHandler:
    def build_warehouse(self, t):
        result = {}
        result['w_id'] = t[0]
        result['w_name'] = t[1]
        result['w_location'] = t[2]
        result['w_budget']= t[3]
        return result

    def build_warehouse_attributes(self, w_id, w_name, w_location, w_budget):
        result = {}
        result['w_id'] = w_id
        result['w_name'] = w_name
        result['w_location'] = w_location
        result['w_budget']= w_budget
        return result
    def buildBestSupplier(self, data):
        result = {}
        result['supplier name'] = data[0]
        result['amount supplied'] = data[1]
        return result
    def buildLowMaterial(self, data):
        result = {}
        result['material'] = data[0]
        result['amount in stock'] = data[1]
        return result
    def buildLeastTransactions(self, data):
        result = {}
        result['cost per day'] = data[0]
        result['day'] = data[1]
        return result

    def buildLeastOutgoing(self, data):
        result = {}
        result['warehouse id'] = data[0]
        result['amount of Outgoing Transactions'] = data[1]
        return result

    def buildMostCities(self, data):
        result = {}
        result['warehouse city'] = data[0]
        result['amount of Transactions'] = data[1]
        return result

    def buildMostIncoming(self, data):
        result = {}
        result['warehouse id'] = data[0]
        result['amount of Incoming Transactions'] = data[1]
        return result

    def buildMostDeliver(self, data):
        result = {}
        result['warehouse id'] = data[0]
        result['Exchanges delivered'] = data[1]
        return result

    def buildReceivesMost(self, data):
        result = {}
        result['User id'] = data[0]
        result['Exchanges recieved'] = data[1]
        return result
    
    def getAllWarehouses(self):
        dao = warehouseDAO()
        dbtuples = dao.getAllWarehouses()
        result = []
        for x in dbtuples:
            result.append(self.build_warehouse(x))
        return jsonify(result)

    def getWarehouseById(self, w_id):
        dao = warehouseDAO()
        result = dao.getWarehouseById(w_id)
        if result:
            return jsonify(self.build_warehouse(result))
        else:
            return jsonify(Error = "Warehouse not found."), 404

    def insertWarehouse(self, data):
        w_name = data['w_name']
        w_location = data['w_location']
        w_budget = data['w_budget']

        if w_name and w_location and w_budget:
            dao = warehouseDAO()
            w_id = dao.insertWarehouse(w_name, w_location, w_budget)
            data['w_id'] = w_id
            return jsonify(data), 201
        else:
            return jsonify(Error = "Unexpected attribute values"), 400
    
    def updateWarehouseById(self, w_id, data):
        w_name = data['w_name']
        w_location = data['w_location']
        w_budget = data['w_budget']

        if w_id and w_name and w_location and w_budget:
            dao = warehouseDAO()
            if not dao.getWarehouseById(w_id):  # if warehouse exist
                return jsonify(Error="Warehouse doesn't exist"), 400
            dao.updateWarehouseById(w_id, w_name, w_location, w_budget)
            return jsonify(data), 200
        else:
            return jsonify(Error = "Unexpected atrribute values"), 400
    
    def deleteByWarehouseId(self, w_id):
        dao = warehouseDAO()
        result = dao.deleteByWarehouseId(w_id)

        if result:
            return jsonify("OK"), 200
        else:
            return jsonify(Error = "Warehouse not found"), 404
    def getLowStock(self, w_id, data):
        dao = warehouseDAO()
        uDAO = UserDAO()
        if not uDAO.inWarehouse(data['u_id'], w_id):
            return jsonify(Error="User not part of warehouse"), 400
        if not dao.getWarehouseById(w_id):
            return jsonify(Error = "Warehouse doesn't exist"), 404
        dtuples = dao.getLowStock(w_id)
        result = []
        for x in dtuples:
            result.append(RacksHandler().build_racks(x))
        return jsonify(Low_Stock=result)

    def getExpensiveRacks(self, w_id, data):
        uDAO = UserDAO()
        dao = warehouseDAO()
        if not dao.getWarehouseById(w_id):
            return jsonify(Error = "Warehouse doesn't exist"), 404
        if not uDAO.inWarehouse(data['u_id'], w_id):
            return jsonify(Error="User not part of warehouse"), 400
        dtuples = dao.getExpensive(w_id)
        result = []
        for x in dtuples:
            result.append(RacksHandler().build_expensive_racks(x))
        return jsonify(Most_Expensive=result)
    def getBottomParts(self, w_id, data):
        uDAO = UserDAO()
        dao = warehouseDAO()
        if not dao.getWarehouseById(w_id):
            return jsonify(Error="Warehouse doesn't exist"), 404
        if not uDAO.inWarehouse(data['u_id'], w_id):
            return jsonify(Error="User not part of warehouse"), 400
        #dao = warehouseDAO()
        dtuples = dao.getBottomParts(w_id)
        result = []
        for x in dtuples:
            result.append(WarehouseHandler().buildLowMaterial(x))
        return jsonify(Lowest_ptype=result)
    def getMostSuppliers(self, w_id, data):
        uDAO = UserDAO()
        dao = warehouseDAO()
        if not dao.getWarehouseById(w_id):
            return jsonify(Error = "Warehouse doesn't exist"), 404
        if not uDAO.inWarehouse(data['u_id'], w_id):
            return jsonify(Error="User not part of warehouse"), 400
        ##dao = warehouseDAO()
        dtuples = dao.getMostSuppliers(w_id)
        result = []
        for x in dtuples:
            result.append(WarehouseHandler().buildBestSupplier(x))
        return jsonify(result)
    def getProfit(self, w_id, data):
        uDAO = UserDAO()
        dao = warehouseDAO()
        if not dao.getWarehouseById(w_id):
            return jsonify(Error="Warehouse doesn't exist"), 404
        if not uDAO.inWarehouse(data['u_id'], w_id):
            return jsonify(Error="User not part of warehouse"), 400
        #dao = warehouseDAO()
        dtuples = dao.getProfit(w_id)
        result = []
        for x in dtuples:
            result.append(x)
        return jsonify(profit=result)
    def getLeastTransactions(self, w_id, data):
        uDAO = UserDAO()
        dao = warehouseDAO()
        if not dao.getWarehouseById(w_id):
            return jsonify(Error="Warehouse doesn't exist"), 404
        if not uDAO.inWarehouse(data['u_id'], w_id):
            return jsonify(Error="User not part of warehouse"), 400
        dtuples = dao.getLeastTransactions(w_id)
        result = []
        for x in dtuples:
            result.append(WarehouseHandler().buildLeastTransactions(x))
        return jsonify(LowestCostsByDay=result)

    def getReceivesMost(self, w_id, data):
        uDAO = UserDAO()
        dao = warehouseDAO()
        if not dao.getWarehouseById(w_id):
            return jsonify(Error="Warehouse doesn't exist"), 404
        if not uDAO.inWarehouse(data['u_id'], w_id):
            return jsonify(Error="User not part of warehouse"), 400
        dtuples = dao.getReceivesMost(w_id)
        result = []
        for x in dtuples:
            result.append(WarehouseHandler().buildReceivesMost(x))
        return jsonify(UsersThatRecieveMost=result)

    def getLeastOutgoing(self):
        dao = warehouseDAO()
        warehouse_list = dao.getLeastOutgoing()
        result_list = []
        for row in warehouse_list:
            result = self.buildLeastOutgoing(row)
            result_list.append(result)
        return jsonify(WarehouseLeastOutgoing=result_list)

    def getMostIncoming(self):
        dao = warehouseDAO()
        warehouse_list = dao.getMostIncoming()
        result_list = []
        for row in warehouse_list:
            result = self.buildMostIncoming(row)
            result_list.append(result)
        return jsonify(WarehouseWithMostIncoming=result_list)
    def getMostCities(self):
        dao = warehouseDAO()
        warehouse_list = dao.getMostCities()
        result_list = []
        for row in warehouse_list:
            result = self.buildMostCities(row)
            result_list.append(result)
        return jsonify(WarehouseWithMostIncoming=result_list)
    def getMostDeliver(self):
        dao = warehouseDAO()
        warehouse_list = dao.getMostDeliver()
        result_list = []
        for row in warehouse_list:
            result = self.buildMostDeliver(row)
            result_list.append(result)
        return jsonify(WarehouseWithMostIncoming=result_list)
       