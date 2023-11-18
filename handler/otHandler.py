from flask import jsonify
from DAO.partsDAO import PartsDAO
from DAO.supplier import SuppliersDAO
from DAO.warehouseDAO import warehouseDAO
from DAO.racksDAO import RacksDao
from DAO.userDAO import UserDAO
from DAO.itDAO import ITDAO
from DAO.otDAO import OTDAO
from DAO.transactionDAO import transactionDAO
class OTHandler:

    def buildOT(self, row):
        result = {}
        result['t_id'] = row[0]
        result['ot_buyername'] = row[1]
        result['ot_sentto'] = row[2]
        result['p_id'] = row[3]
        result['w_id'] = row[4]
        result['u_id'] = row[5]
        return result
    def buildOTAttirbutes(self, t_id, ot_buyername, ot_sentto, p_id, w_id, u_id):
        result = {}
        result['t_id'] = t_id
        result['ot_buyername'] = ot_buyername
        result['ot_sentto'] = ot_sentto
        result['p_id'] = p_id
        result['w_id'] = w_id
        result['u_id'] = u_id
        return result


    def getAllOT(self):
        dao = OTDAO()
        OTList = dao.getAllOT()
        ResultsOT = []
        for row in OTList:
            result = self.buildOT(row)
            ResultsOT.append(result)
        return jsonify(Outgoing_Transactions=ResultsOT)

    def getOT(self, ot_id):
        dao = OTDAO()
        row = dao.getOT(ot_id)
        if not row:
            return jsonify(Error='Outgoing Transaction not found'), 404
        else:
            OT = self.buildOT(row)
            return jsonify(Incoming_Transactions=OT)
    def insertOT(self, data):
        uDAO = UserDAO()
        rDAO = RacksDao()
        wDAO = warehouseDAO()
        #sDAO = SuppliersDAO()
        pDAO = PartsDAO()
        if not uDAO.getUserById(data['u_id']):  # if user exist
            return jsonify(Error="User doesn't exist"), 400
        #if not supDAO.supplies(data['p_id'], data['s_id']):
            #return jsonify(Error="Supplier does not supply part specified"), 400
        if not wDAO.getWarehouseById(data['w_id']):  # if warehouse exist
            return jsonify(Error="Warehouse doesn't exist"), 400
        if not uDAO.inWarehouse(data['u_id'], data['w_id']):
            return jsonify(Error="User not part of warehouse"), 400
        #if not sDAO.searchById(data['s_id']):  # if supplier exist
            #return jsonify(Error="Supplier doesn't exist"), 400
        if not pDAO.getPart(data['p_id']):  # if part exists
            return jsonify(Error="Part doesn't exist"), 400
        if not wDAO.partInStock(data['w_id'], data['p_id']) or sum(rDAO.getAmount(wDAO.partInStock(data['w_id'], data['p_id']))) <= int(data['t_quantity']):
            return jsonify(Error="Part not in warehouse"), 400
        else:
            rDAO.lowerAmount(wDAO.partInStock(data['w_id'], data['p_id']), data['t_quantity'])
            wDAO.addBudget(data['w_id'], data['t_value'])
        #it_id = data['it_id']
        ot_buyername = data['ot_buyername']
        ot_sentto = data['ot_sentto']
        t_date = data['t_date']
        t_value = data['t_value']
        t_quantity = data['t_quantity']
        #s_id = data['s_id']
        p_id = data['p_id']
        w_id = data['w_id']
        #r_id = data['r_id']
        u_id = data['u_id']
        tDAO = transactionDAO()
        t_id = tDAO.insertTransaction(t_date, t_value, t_quantity)
        if ot_buyername and ot_sentto and p_id and w_id and u_id:
            dao = OTDAO()
            ot_id = OTDAO().insertOT(ot_buyername, ot_sentto, p_id, w_id, u_id)
            result = self.buildOTAttirbutes(t_id,ot_buyername, ot_sentto, p_id, w_id, u_id)
            return jsonify(Outgoing_Transactions=result), 201
        else:
            jsonify(Error="Unexpected attributes in post Request"), 400
    def updateOT(self, ot_id, data):
        dao = OTDAO()
        uDAO = UserDAO()
        rDAO = RacksDao()
        wDAO = warehouseDAO()
        #sDAO = SuppliersDAO()
        pDAO = PartsDAO()
        if not uDAO.getUserById(data['u_id']):
            return jsonify(Error="User doesn't exist"), 402
        #if not rDAO.getRacksById(data['r_id']):
            #return jsonify(Error="Rack doesn't exist"), 402
        if not wDAO.getWarehouseById(data['w_id']):
            return jsonify(Error="Warehouse doesn't exist"), 402
        #if not sDAO.searchById(data['s_id']):
            #return jsonify(Error="Supplier doesn't exist"), 402
        if not pDAO.getPart(data['p_id']):
            return jsonify(Error="Part doesn't exist"), 402
        else:
            if len(data) != 8:
                print(len(data))
                return jsonify(Error = "Malformed update request."), 400
            else:
                ot_buyername = data['ot_buyername']
                ot_placesent = data['ot_placesent']
                t_date = data['t_date']
                t_value = data['t_value']
                t_quantity = data['t_quantity']
                #s_id = data['s_id']
                p_id = data['p_id']
                w_id = data['w_id']
                #r_id = data['r_id']
                u_id = data['u_id']
                if ot_buyername and ot_placesent and t_date and t_value and t_quantity and p_id and w_id and r_id and u_id:
                    dao.updateOT(ot_id, ot_buyername, ot_placesent, t_date, t_value, t_quantity, p_id, w_id, r_id, u_id)
                    result = self.buildOTAttirbutes(ot_id, ot_buyername, ot_placesent, t_date, t_value, t_quantity, p_id, w_id, r_id, u_id)
                    return jsonify(Incoming_transaction=result), 200
                else:
                    return jsonify(Error='Unexpected attributes in update request.'), 400

        # it_id = data['it_id']



