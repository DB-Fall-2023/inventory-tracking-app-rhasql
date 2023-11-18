from flask import jsonify
from DAO.transactionDAO import transactionDAO

class transactionHandler:

    def buildT(self, row):
        result = {}
        result['t_id'] = row[0]
        result['t_date'] = row[1]
        result['t_value'] = row[2]
        result['t_quantity'] = row[3]
        return result
    def buildTAttirbutes(self, t_id, t_date, t_value, t_quantity):
        result = {}
        result['t_id'] = t_id
        result['t_date'] = t_date
        result['t_value'] = t_value
        result['t_quantity'] = t_quantity
        return result
    def insertT(self, data):
        t_date = data['t_date']
        t_value = data['t_value']
        t_quantity = data['t_quantity']
        if t_date and t_value and t_quantity:
            dao = transactionDAO()
            t_id = dao.insertTransaction(t_date, t_value, t_quantity)
            return t_id
        return jsonify(Error="Unexpected attributes in post Request"), 400
