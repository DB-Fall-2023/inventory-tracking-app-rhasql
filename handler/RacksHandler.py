from flask import jsonify
from DAO.racksDAO import RacksDao

class RacksHandler:

    def build_racks(self, row):
        result = {}
        result['r_id'] = row[0]
        result['r_capacity'] = row[1]
        result['r_fullCost'] = row[2]
        result['r_partsinstock'] = row[3]
        return result
    
    def buildRacksAttributes(self, r_id, r_capacity, r_fullCost, r_partsinstock):
        result = {}
        result['r_id'] = r_id
        result['r_capacity'] = r_capacity
        result['r_fullCost'] = r_fullCost
        result['r_partsinstock'] = r_partsinstock
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
        r_capacity = data['r_capacity']
        r_fullCost = data['r_fullCost']
        r_partsinstock = data['r_partsinstock']

        if r_capacity and r_fullCost and r_partsinstock:
            dao = RacksDao()
            r_id = dao.insertRack(r_capacity, r_fullCost, r_partsinstock)
            result = self.buildRacksAttributes(r_id, r_capacity, r_fullCost, r_partsinstock)
            return jsonify(racks = result), 201
        else: jsonify(Error = "Unexpected attributes in post Request"), 400

    def updateRack(self , r_id, data):
        dao = RacksDao()
        if not dao.getRacksById(r_id):
            return jsonify(Error = "Rack not found."), 404
        else:
            if len(data) != 3:
                print(len(data))
                return jsonify(Error = "Malformed update request."), 400
            else:
                r_capacity = data['r_capacity']
                r_fullcost = data['r_fullcost']
                r_partsinstock = data['r_partsinstock']
                if r_capacity and r_fullcost and r_partsinstock:
                    dao.updateRack(r_id, r_capacity, r_fullcost, r_partsinstock)
                    result = self.buildRacksAttributes(r_id, r_capacity, r_fullcost, r_partsinstock)
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