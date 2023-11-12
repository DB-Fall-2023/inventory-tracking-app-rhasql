from flask import jsonify
from DAO.warehouseDAO import warehouseDAO

class WarehouseHandler:
    def build_warehouse(self, t):
        result = {}
        result['w_id'] = t[0]
        result['w_name'] = t[1]
        result['w_location'] = t[2]
        return result

    def build_warehouse_attributes(self, w_id, w_name, w_location):
        result = {}
        result['w_id'] = w_id
        result['w_name'] = w_name
        result['w_location'] = w_location
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

        if w_name and w_location:
            dao = warehouseDAO()
            w_id = dao.insertWarehouse(w_name, w_location)
            data['w_id'] = w_id
            return jsonify(data), 201
        else:
            return jsonify(Error = "Unexpected attribute values"), 400
    
    def updateWarehouseById(self, w_id, data):
        w_name = data['w_name']
        w_location = data['w_location']

        if w_id and w_name and w_location:
            dao = warehouseDAO()
            flag = dao.updateWarehouseById(w_id, w_name, w_location)

            if flag:
                return jsonify(data), 200
            else:
                return jsonify(Error = "Not found"), 404
        else:
            return jsonify(Error = "Unexpected atrribute values"), 400
    
    def deleteByWarehouseId(self, w_id):
        dao = warehouseDAO()
        result = dao.deleteByWarehouseId(w_id)

        if result:
            return jsonify("OK"), 200
        else:
            return jsonify(Error = "Warehouse not found"), 404
            

       