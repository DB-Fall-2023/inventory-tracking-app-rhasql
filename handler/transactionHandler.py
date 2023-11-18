from flask import jsonify
from DAO.transactionDAO import transactionDAO

class transactionHandler:

    def buildT(self, row):
        result = {}
        result['t_id'] = row[0]
        result['t_date'] = row[1]
        result['t_value'] = row[2]
        result['t_quantity'] = row[3]
        result['u_id'] = row[4]
        result['w_id'] = row[5]
        result['p_id'] = row[6]
        return result
    def buildTAttirbutes(self, t_id, t_date, t_value, t_quantity, u_id, w_id, p_id):
        result = {}
        result['t_id'] = t_id
        result['t_date'] = t_date
        result['t_value'] = t_value
        result['t_quantity'] = t_quantity
        result['u_id'] = u_id
        result['w_id'] = w_id
        result['p_id'] = p_id
        return result
    def insertT(self, data):
        t_date = data['t_date']
        t_value = data['t_value']
        t_quantity = data['t_quantity']
        u_id = data['u_id']
        w_id = data['w_id']
        p_id = data['p_id']
        if t_date and t_value and t_quantity and u_id and w_id and p_id:
            dao = transactionDAO()
            t_id = dao.insertTransaction(t_date, t_value, t_quantity, u_id, w_id, p_id)
            return t_id
        return jsonify(Error="Unexpected attributes in post Request"), 400
