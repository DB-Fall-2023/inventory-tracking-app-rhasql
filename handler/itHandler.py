from flask import jsonify
from DAO.partsDAO import PartsDAO
from DAO.supplier import SuppliersDAO
from DAO.warehouseDAO import warehouseDAO
from DAO.racksDAO import RacksDao
from DAO.userDAO import UserDAO
from DAO.itDAO import ITDAO
class ITHandler:

    def buildIT(self, row):
        result = {}
        result['it_id'] = row[0]
        result['t_date'] = row[1]
        result['t_value'] = row[2]
        result['t_quantity'] = row[3]
        result['s_id'] = row[4]
        result['p_id'] = row[5]
        result['w_id'] = row[6]
        result['r_id'] = row[7]
        result['u_id'] = row[8]
        return result
    def buildITAttirbutes(self, it_id, t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id):
        result = {}
        result['it_id'] = it_id
        result['t_date'] = t_date
        result['t_value'] = t_value
        result['t_quantity'] = t_quantity
        result['s_id'] = s_id
        result['p_id'] = p_id
        result['w_id'] = w_id
        result['r_id'] = r_id
        result['u_id'] = u_id
        return result


    def getAllIT(self):
        dao = ITDAO()
        ITList = dao.getAllIT()
        ResultsIT = []
        for row in ITList:
            result = self.buildIT(row)
            ResultsIT.append(result)
        return jsonify(Incoming_Transactions=ResultsIT)

    def getIT(self, it_id):
        dao = ITDAO()
        row = dao.getIT(it_id)
        if not row:
            return jsonify(Error='Incoming Transaction not found'), 404
        else:
            IT = self.buildIT(row)
            return jsonify(Incoming_Transactions=IT)
    def insertIT(self, data):
        uDAO = UserDAO()
        rDAO = RacksDao()
        wDAO = warehouseDAO()
        sDAO = SuppliersDAO()
        pDAO = PartsDAO()
        if not uDAO.getUserById(data['u_id']):
            return jsonify(Error="User doesn't exist"), 402
        if not rDAO.getRacksById(data['r_id']):
            return jsonify(Error="Rack doesn't exist"), 402
        if not wDAO.getWarehouseById(data['w_id']):
            return jsonify(Error="Warehouse doesn't exist"), 402
        if not sDAO.searchById(data['s_id']):
            return jsonify(Error="Supplier doesn't exist"), 402
        if not pDAO.getPart(data['p_id']):
            return jsonify(Error="Part doesn't exist"), 402
        #it_id = data['it_id']
        t_date = data['t_date']
        t_value = data['t_value']
        t_quantity = data['t_quantity']
        s_id = data['s_id']
        p_id = data['p_id']
        w_id = data['w_id']
        r_id = data['r_id']
        u_id = data['u_id']
        if t_date and t_value and t_quantity and s_id and p_id and w_id and r_id and u_id:
            dao = ITDAO()
            it_id = ITDAO().insertIT(t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id)
            result = self.buildITAttirbutes(it_id,t_date,t_value,t_quantity,s_id,p_id,w_id,r_id,u_id)
            return jsonify(Incoming_Transactions=result), 201
        else:
            jsonify(Error="Unexpected attributes in post Request"), 400
    def updateIT(self, it_id, data):
        dao = ITDAO()
        uDAO = UserDAO()
        rDAO = RacksDao()
        wDAO = warehouseDAO()
        sDAO = SuppliersDAO()
        pDAO = PartsDAO()
        if not uDAO.getUserById(data['u_id']):
            return jsonify(Error="User doesn't exist"), 402
        if not rDAO.getRacksById(data['r_id']):
            return jsonify(Error="Rack doesn't exist"), 402
        if not wDAO.getWarehouseById(data['w_id']):
            return jsonify(Error="Warehouse doesn't exist"), 402
        if not sDAO.searchById(data['s_id']):
            return jsonify(Error="Supplier doesn't exist"), 402
        if not pDAO.getPart(data['p_id']):
            return jsonify(Error="Part doesn't exist"), 402
        else:
            if len(data) != 8:
                print(len(data))
                return jsonify(Error = "Malformed update request."), 400
            else:
                t_date = data['t_date']
                t_value = data['t_value']
                t_quantity = data['t_quantity']
                s_id = data['s_id']
                p_id = data['p_id']
                w_id = data['w_id']
                r_id = data['r_id']
                u_id = data['u_id']
                if t_date and t_value and t_quantity and s_id and p_id and w_id and r_id and u_id:
                    dao.updateIT(it_id, t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id)
                    result = self.buildITAttirbutes(it_id, t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id)
                    return jsonify(Incoming_transaction=result), 200
                else:
                    return jsonify(Error='Unexpected attributes in update request.'), 400

        # it_id = data['it_id']



