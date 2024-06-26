from flask import jsonify
from DAO.supplier import SuppliersDAO

class SupplierHandler:

    def mapToDict(self, t):
        result = {}
        result['Id'] = t[0]
        result['Name'] = t[1]
        result['City'] = t[2]
        result['Phone'] = t[3]

        return result

    def getAllSuppliers(self):
        dao = SuppliersDAO()
        dbtuples = dao.getAllSuppliers()
        result = []

        for e in dbtuples:
            result.append(self.mapToDict(e))

        return jsonify(result)

    def searchById(self, sid):
        dao = SuppliersDAO()
        result = dao.searchById(sid)
        if result :
            return jsonify(self.mapToDict(result))
        else:
            return jsonify(Error="Not Found"), 404

    def insertSupplier(self, data):
        if len(data) != 3:
            return jsonify(Error="Malformed request"), 404
        name = data['s_name']
        city = data['s_city']
        phone = data['s_phone']


        if name and city and phone:
            dao = SuppliersDAO()
            sid = dao.insertSupplier(name, city, phone)
            data['s_id'] = sid
            return jsonify(data), 201

        else:
            return jsonify(Error="Unexpected attribute values"), 400

    def deleteById(self, sid):
        dao = SuppliersDAO()
        result = dao.deleteById(sid)

        if result :
            return jsonify("OK"), 200
        else:
            return jsonify(Error="Supplier Not Found"), 404

    def updateById(self, sid, data):
        if len(data) != 3 or not SupplierHandler().searchById(sid):
            return jsonify(Error="Malformed request"), 404
        name = data['Name']
        city = data['City']
        phone = data['Phone']
        if sid and city and phone:
            dao = SuppliersDAO()
            flag = dao.updateById(sid, name, city, phone)

            if flag:
                return jsonify(data), 200
            else:
                return jsonify(Error="Not found"), 404

        else:
            return jsonify("Unexpected attribute values"), 400


