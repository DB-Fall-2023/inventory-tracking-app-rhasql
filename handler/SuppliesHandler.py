from flask import jsonify
from DAO.SuppliesDAO import SuppliesDAO
from DAO.partsDAO import PartsDAO
from DAO.supplier import SuppliersDAO

class SuppliesHandler:

    def mapToDict(self, t):
        result = {}
        result['p_id'] = t[0]
        result['s_id'] = t[1]
        result['stock'] = t[2]
        return result

    # Costructs dictionary of attributes
    def mapDictSupplied(self, t):
        result = {}
        result['p_name'] = t[0]
        result['stock'] = t[1]
        return result
    def build_supplies_attributes(self, p_id, s_id, stock):
        result = {}
        result['p_id'] = p_id
        result['s_id'] = s_id
        result['stock'] = stock
        return result
    def getAllSupplies(self):
        dao = SuppliesDAO()
        dtuples = dao.getAllSupplies()
        result = []
        for x in dtuples:
            result.append(self.mapToDict(x))
        return jsonify(result)
    def addSupplies(self, json):
        pDAO = PartsDAO()
        sDAO = SuppliersDAO()
        if not pDAO.getPart(json['p_id']):
            return jsonify(Error="Part doesn't exist"), 402
        if not sDAO.searchById(json['s_id']):
            return jsonify(Error="Supplier doesn't exist"), 402
        p_id = json['p_id']
        s_id = json['s_id']
        stock = json['stock']
        if s_id and p_id and stock:
            dao = SuppliesDAO()
            dao.insertSupplies(p_id, s_id, stock)
            result = self.build_supplies_attributes(p_id, s_id, stock)
            return jsonify(Supplies=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def getSupplies(self,p_id, s_id):
        pDAO = PartsDAO()
        sDAO = SuppliersDAO()
        dao = SuppliesDAO()
        if not pDAO.getPart(p_id):
            return jsonify(Error="Part doesn't exist"), 402
        if not sDAO.searchById(s_id):
            return jsonify(Error="Supplier doesn't exist"), 402
        dao = SuppliesDAO()
        dtuple = dao.getSupplies(p_id,s_id)
        if not dtuple:
            return jsonify(Error="Supplies doesn't exist"), 402
        supplies =self.mapToDict(dtuple)
        return jsonify(Supplies=supplies)
    def updateSupplies(self,p_id,s_id,json):
        pDAO = PartsDAO()
        sDAO = SuppliersDAO()
        dao = SuppliesDAO()
        if not pDAO.getPart(p_id):
            return jsonify(Error="Part doesn't exist"), 402
        if not sDAO.searchById(s_id):
            return jsonify(Error="Supplier doesn't exist"), 402
        if(len(json)!=3):
            return jsonify(Error="Improperly constructed request"), 400
        stock = json['stock']
        if stock:
            dao.updateSupplies(p_id, s_id, stock)
            result = self.build_supplies_attributes(p_id, s_id, stock)
            return jsonify(Supplies=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400
    def deleteSupplies(self, p_id, s_id):
        pDAO = PartsDAO()
        sDAO = SuppliersDAO()
        dao = SuppliesDAO()
        if not pDAO.getPart(p_id):
            return jsonify(Error="Part doesn't exist"), 402
        if not sDAO.searchById(s_id):
            return jsonify(Error="Supplier doesn't exist"), 402
        else:
            ids = dao.deleteSupplies(p_id,s_id)
            return jsonify(DeleteStatus="OK"), 200

    def getSupplierSupplies(self, s_id):
        dao = SuppliesDAO()
        sDAO = SuppliersDAO()
        if not sDAO.searchById(s_id):
            return jsonify(Error="Supplier doesn't exist"), 402
        else:
            dtuples = dao.getSupplierSupplies(s_id)
            result = []
            for x in dtuples:
                result.append(self.mapDictSupplied(x))
            return jsonify(result)
