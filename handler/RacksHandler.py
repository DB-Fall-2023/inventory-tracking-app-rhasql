from flask import jsonify
from DAO.racksDAO import RacksDao
from DAO.warehouseDAO import warehouseDAO
from DAO.partsDAO import PartsDAO

class RacksHandler:

    def build_racks(self, row):
        result = {}
        result['r_id'] = row[0]
        result['r_amount'] = row[1]
        #result['r_capacity'] = row[2]
        #result['r_partsinstock'] = row[3]
        result['w_id'] = row[2]
        result['p_id'] = row[3]
        result['r_capacity'] = row[4]
        return result
    
    def buildRacksAttributes(self, r_id, r_amount, w_id, p_id, r_capacity):
        result = {}
        result['r_id'] = r_id
        result['r_amount'] = r_amount
        result['r_capacity'] = r_capacity
        result['w_id'] = w_id
        result['p_id'] = p_id
        return result
    def build_expensive_racks(self, row):
        result = {}
        result['r_id'] = row[0]
        result['r_amount'] = row[1]
        #result['r_capacity'] = row[2]
        #result['r_partsinstock'] = row[3]
        result['w_id'] = row[2]
        result['p_id'] = row[3]
        result['r_capacity'] = row[4]
        result['total_price'] = row[5]
        return result
    
    def getAllRacks(self):
        dao = RacksDao()
        racksList = dao.getAllRacks()
        ResultsRacks = []
        for row in racksList:
            result = self.build_racks(row)
            ResultsRacks.append(result)
        return jsonify(racks = ResultsRacks)
    
    def getRacksById(self, r_id):
        dao = RacksDao()
        row = dao.getRacksById(r_id)
        if not row:
            return jsonify(Error = 'Rack not found'), 404
        else:
            Racks = self.build_racks(row)
            return jsonify(racks = Racks)
    
    def insertRack(self, data):
        pDAO = PartsDAO()
        wDAO = warehouseDAO()
        if not pDAO.getPart(data['p_id']):
            return jsonify(Error="Part doesn't exist"), 402
        if not wDAO.getWarehouseById(data['w_id']):
            return jsonify(Error="Warehouse doesn't exist"), 402
        if data['r_amount'] > data['r_capacity']:
            return jsonify(Error="Cannot add amount greater than capacity"), 402
        r_capacity = data['r_capacity']
        r_amount = data['r_amount']
        p_id = data['p_id']
        w_id = data['w_id']
        #r_fullCost = data['r_fullCost']
        #r_partsinstock = data['r_partsinstock']

        if p_id and w_id and r_amount and r_capacity:
            dao = RacksDao()
            r_id = dao.insertRack(r_amount, w_id, p_id, r_capacity)
            result = self.buildRacksAttributes(r_id, r_amount, w_id, p_id, r_capacity)
            return jsonify(racks = result), 201
        else: jsonify(Error = "Unexpected attributes in post Request"), 400

    def updateRack(self , r_id, data):
        dao = RacksDao()
        pDAO = PartsDAO()
        wDAO = warehouseDAO()
        if not dao.getRacksById(r_id):
            return jsonify(Error = "Rack not found."), 404
        if not pDAO.getPart(data['p_id']):
            return jsonify(Error="Part doesn't exist"), 402
        if not wDAO.getWarehouseById(data['w_id']):
            return jsonify(Error="Warehouse doesn't exist"), 402
        if data['r_amount'] > data['r_capacity']:
            return jsonify(Error="Cannot add amount greater than capacity"), 402

        else:
            if len(data) != 4:
                print(len(data))
                return jsonify(Error = "Malformed update request."), 400
            else:
                r_amount = data['r_amount']
                r_capacity = data['r_capacity']
                w_id = data['w_id']
                p_id = data['p_id']
                if r_amount and w_id and p_id:
                    dao.updateRack(r_id, r_amount, w_id, p_id,  r_capacity)
                    result = self.buildRacksAttributes(r_id, r_amount, w_id, p_id,  r_capacity)
                    return jsonify(racks = result), 200
                else:
                    return jsonify(Error = 'Unexpected attributes in update request.'), 400
    
    def deleteRack(self, r_id):
        dao = RacksDao()
        if not dao.getRacksById(r_id):
            return jsonify(Error = 'Rack not found.'), 404
        else:
            dao.deleteRack(r_id)
            return jsonify(DeleteState = 'Success')