from flask import jsonify
from DAO.partsDAO import PartsDAO
from DAO.supplier import SuppliersDAO
from DAO.SuppliesDAO import SuppliesDAO
from DAO.warehouseDAO import warehouseDAO
from DAO.racksDAO import RacksDao
from DAO.userDAO import UserDAO
from DAO.itDAO import ITDAO
from DAO.transactionDAO import transactionDAO
from handler.transactionHandler import transactionHandler
class ITHandler:

    def buildIT(self, row):
        result = {}
        result['t_id'] = row[0]
        result['t_date'] = row[1]
        result['t_value'] = row[2]
        result['t_quantity'] = row[3]
        result['s_id'] = row[4]
        result['p_id'] = row[5]
        result['w_id'] = row[6]
        result['r_id'] = row[7]
        result['u_id'] = row[8]
        return result
    def buildITAttirbutes(self, t_id, t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id):
        result = {}
        result['t_id'] = t_id
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

    def getIT(self, t_id):
        dao = ITDAO()
        row = dao.getIT(t_id)
        if not row:
            return jsonify(Error='Incoming Transaction not found'), 404
        else:
            IT = self.buildIT(row)
            return jsonify(Incoming_Transactions=IT)
    def insertIT(self, data):
        uDAO = UserDAO() #if user belongs to warehouse
        rDAO = RacksDao() #if rack exists in warehouse (create it if not)
        wDAO = warehouseDAO() #if rack exists in warehouse, if warehouse had budget to make purchase
        sDAO = SuppliersDAO() #supplies part
        pDAO = PartsDAO()
        supDAO = SuppliesDAO()
        if not uDAO.getUserById(data['u_id']): #if user exist
            return jsonify(Error="User doesn't exist"), 400
        if not uDAO.inWarehouse(data['u_id'], data['w_id']):
            return jsonify(Error="User not part of warehouse"), 400
        if not supDAO.supplies(data['p_id'], data['s_id']):
            return jsonify(Error="Supplier does not supply part specified"), 400
        if not wDAO.getWarehouseById(data['w_id']): #if warehouse exist
            return jsonify(Error="Warehouse doesn't exist"), 400
        if not sDAO.searchById(data['s_id']): #if supplier exist
            return jsonify(Error="Supplier doesn't exist"), 400
        if not pDAO.getPart(data['p_id']): #if part exists
            return jsonify(Error="Part doesn't exist"), 400
        if rDAO.getRacksById(data['r_id']): #if rack exists
            print("har")
            if wDAO.partIn(data['w_id'], data['p_id'], data['r_id']): #if rack has x part
                if(sum(rDAO.getAmount(data['r_id'])) + int(data['t_quantity']) >  sum(rDAO.getCapacity(data['r_id']))): #if amount added surpases rack capacity
                    return jsonify(Error="Rack capacity exceeded"), 400
                else: #quantity gets added to rack
                    if (sum(wDAO.getBudget(data['w_id'])) < int(data['t_value'])):
                        return jsonify(Error="Could not purchase, budget too low"), 400
                    else:
                        rDAO.updateAmount(data['r_id'], data['t_quantity'])  # update amount of parts in rack and update budget
                        wDAO.updateBudget(data['w_id'], data['t_value'])
                        r_id = data['r_id']
            else: #return error if rack selecte doesn't contain x item
                return jsonify(Error="Incorrect Rack selected"), 400
        else:
            if wDAO.partInStock(data['w_id'], data['p_id']): #if part in SOME rack in da warehouse
                return jsonify(Error="Incorrect Rack selected"), 400
            else: #if rack doesn't exist
                print("oh holera")
                r_id = rDAO.insertRack(data['t_quantity'], data['w_id'], data['p_id'], data['t_quantity'])




                #add quantity to rack

        # if not wDAO.partIn(data['w_id'], data['p_id']):
        #     rDAO.insertRack(data['t_quantity'], data['w_id'], data['p_id'], data['t_quantity'])
        # else:

        #if not rDAO.getRacksById(data['r_id']):
            #if pDAO.getPart(data['p_id']) and not wDAO.partIn(data['w_id'], data['p_id']):
                #r_id = rDAO.insertRack(data['t_quantity'], data['w_id'], data['p_id'],data['t_quantity'])
            #return jsonify(Error='lol'), 404

        tDAO = transactionDAO()
        t_id = tDAO.insertTransaction(data['t_date'], data['t_value'], data['t_quantity'], data['u_id'], data['w_id'], data['p_id'])
        #it_id = data['it_id']
        t_date = data['t_date']
        t_value = data['t_value']
        t_quantity = data['t_quantity']
        s_id = data['s_id']
        p_id = data['p_id']
        w_id = data['w_id']
        u_id = data['u_id']
        if t_id and t_value and t_date and t_quantity and s_id and r_id and p_id and w_id  and u_id:
            dao = ITDAO()
            it_id = ITDAO().insertIT(t_id, s_id, r_id)
            result = self.buildITAttirbutes(t_id,t_date,t_value,t_quantity,s_id,p_id,w_id, r_id,u_id)
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



