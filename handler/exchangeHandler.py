from flask import jsonify
from DAO.exchangeDAO import ExchangeDAO
from DAO.partsDAO import PartsDAO
from DAO.supplier import SuppliersDAO
from DAO.SuppliesDAO import SuppliesDAO
from DAO.warehouseDAO import warehouseDAO
from DAO.racksDAO import RacksDao
from DAO.userDAO import UserDAO
from DAO.transactionDAO import transactionDAO

class ExchangeHandler:
    def buildExchange(self, row):
        result = {}
        result['t_id'] = row[0]
        result['sender_u_id'] = row[1]
        result['sender_w_id'] = row[2]
        result['sender_p_id'] = row[3]
        result['sender_r_id'] = row[4]
        result['receiver_r_id'] = row[5]
        result['receiver_quantity'] = row[6]
        result['t_date'] = row[7]
        result['t_value'] = row[8]
        result['t_quantity'] = row[9]
        result['u_id'] = row[10]
        result['w_id'] = row[11]
        result['p_id'] = row[12]

        return result

    def buildExchangeAttributes(self, t_id, sender_u_id, sender_w_id, sender_p_id, sender_r_id, receiver_r_id, receiver_quantity, t_date, t_value, t_quantity, u_id, w_id, p_id):
        result = {}
        result['t_id'] = t_id
        result['sender_u_id'] = sender_u_id
        result['sender_w_id'] = sender_w_id
        result['sender_p_id'] = sender_p_id
        result['sender_r_id'] = sender_r_id
        result['receiver_r_id'] = receiver_r_id
        result['receiver_quantity'] = receiver_quantity
        result['t_date'] = t_date
        result['t_value'] = t_value
        result['t_quantity'] = t_quantity
        result['u_id'] = u_id
        result['w_id'] = w_id
        result['p_id'] = p_id
        return result

    def getAllExchange(self):
        dao = ExchangeDAO()
        exchangeList = dao.getAllExchange()
        resultsExchange = []
        for row in exchangeList:
            result = self.buildExchange(row)
            resultsExchange.append(result)
        return jsonify(Exchange=resultsExchange)

    def getExchangeById(self,t_id):
        dao = ExchangeDAO()
        row = dao.getExchangeById(t_id)
        if not row:
            return jsonify(Error="Exchange Transaction not found"), 404
        else:
            exchange = self.buildExchange(row)
            return jsonify(Exchange=exchange)

    def insertExchange(self, data):
        uDAO = UserDAO() #if user belongs to warehouse
        rDAO = RacksDao() #if rack exists in warehouse (create it if not)
        wDAO = warehouseDAO() #if rack exists in warehouse, if warehouse had budget to make purchase
        pDAO = PartsDAO()
        if not uDAO.getUserById(data['u_id']) or not uDAO.getUserById(data['sender_u_id']): #if user exist
            return jsonify(Error="User doesn't exist"), 400
        if not uDAO.inWarehouse(data['u_id'], data['w_id']) or not uDAO.inWarehouse(data['sender_u_id'], data['sender_w_id']):
            return jsonify(Error="User not part of warehouse"), 400
        if not wDAO.getWarehouseById(data['w_id']) or not wDAO.getWarehouseById(data['sender_w_id']): #if warehouse exist
            return jsonify(Error="Warehouse doesn't exist"), 400
        if not pDAO.getPart(data['p_id']) or not pDAO.getPart(data['sender_p_id']): #if part exists
            return jsonify(Error="Part doesn't exist"), 400
        if rDAO.getRacksById(data['receiver_r_id']) and rDAO.getRacksById(data['sender_r_id']): #if rack exists
            if wDAO.partIn(data['w_id'], data['p_id'], data['receiver_r_id']) and wDAO.partIn(data['sender_w_id'], data['sender_p_id'], data['sender_r_id']):
                if not wDAO.allPartIn(data['w_id'], data['sender_p_id']):
                    rDAO.insertRack(data['t_quantity'], data['w_id'], data['sender_p_id'], data['t_quantity'])
                if not wDAO.allPartIn(data['sender_w_id'], data["p_id"]):
                    rDAO.insertRack(data['receiver_quantity'], data['sender_w_id'], data['p_id'], data['receiver_quantity'])
                if ( (sum(rDAO.getAmount(data['receiver_r_id'])) + int(data['t_quantity']) > sum(rDAO.getCapacity(data['receiver_r_id']))) and (sum(rDAO.getAmount(data['sender_r_id'])) + int(data['receiver_quantity']) > sum(rDAO.getCapacity(data['sender_r_id']))) ):  # if amount added surpases rack capacity
                    return jsonify(Error="Rack capacity exceeded"), 400
                else:  # quantity gets added to rack
                    if (sum(wDAO.getBudget(data['w_id'])) < int(data['t_value'])) and (sum(wDAO.getBudget(data['sender_w_id'])) < int(data['t_value'])):
                        return jsonify(Error="Could not purchase, budget too low"), 400
                    else:
                        rDAO.updateAmount(data['receiver_r_id'], data['receiver_quantity'])  # update amount of parts in rack and update budget
                        rDAO.updateAmount(data['sender_r_id'], data['t_quantity'])  # update amount of parts in rack and update budget

                        wDAO.updateBudget(data['w_id'], data['t_value'])
                        wDAO.updateBudget(data['sender_w_id'], data['t_value'])

            else:  # return error if rack selected doesn't contain x item
                return jsonify(Error="Incorrect Rack selected"), 400
        else:
            if wDAO.partInStock(data['w_id'], data['p_id']) and wDAO.partInStock(data['sender_w_id'], data['sender_p_id']): #if part in SOME rack in the warehouse
                return jsonify(Error="Incorrect Rack selected"), 400
            elif not rDAO.getRacksById(data['receiver_r_id']):
                reciever_r_id = rDAO.insertRack(data['t_quantity'], data['w_id'], data['p_id'], data['t_quantity'])
            else:
                sender_r_id = rDAO.insertRack(data['t_quantity'], data['w_id'], data['p_id'], data['t_quantity'])


        sender_u_id = data['sender_u_id']
        sender_w_id = data['sender_w_id']
        sender_p_id = data['sender_p_id']
        sender_r_id = data['sender_r_id']
        receiver_r_id = data['receiver_r_id']
        receiver_quantity = data['receiver_quantity']
        t_date = data['t_date']
        t_value = data['t_value']
        t_quantity = data['t_quantity']
        u_id = data['u_id']
        w_id = data['w_id']
        p_id = data['p_id']
        tDAO = transactionDAO()
        t_id = tDAO.insertTransaction(data['t_date'], data['t_value'], data['t_quantity'], data['u_id'], data['w_id'], data['p_id'])
        if t_id and t_value and t_date and t_quantity and sender_u_id and sender_w_id and sender_p_id and sender_r_id and receiver_r_id and receiver_quantity:
            dao = ExchangeDAO()
            it_id = ExchangeDAO().insertExchange(t_id, sender_u_id, sender_w_id, sender_p_id, sender_r_id, receiver_r_id, receiver_quantity)
            result = self.buildExchangeAttributes(t_id, sender_u_id, sender_w_id, sender_p_id, sender_r_id, receiver_r_id, receiver_quantity, t_date, t_value, t_quantity, u_id, w_id, p_id)
            return jsonify(Exchange_Transactions=result), 201
        else:
            jsonify(Error="Unexpected attributes in post Request"), 400

    def updateExchange(self,t_id, data):
        uDAO = UserDAO()  # if user belongs to warehouse
        rDAO = RacksDao()  # if rack exists in warehouse (create it if not)
        wDAO = warehouseDAO()  # if rack exists in warehouse, if warehouse had budget to make purchase
        pDAO = PartsDAO()
        if not uDAO.getUserById(data['u_id']) or not uDAO.getUserById(data['sender_u_id']):  # if user exist
            return jsonify(Error="User doesn't exist"), 400
        if not uDAO.inWarehouse(data['u_id'], data['w_id']) or not uDAO.inWarehouse(data['sender_u_id'],
                                                                                    data['sender_w_id']):
            return jsonify(Error="User not part of warehouse"), 400
        if not wDAO.getWarehouseById(data['w_id']) or not wDAO.getWarehouseById(
                data['sender_w_id']):  # if warehouse exist
            return jsonify(Error="Warehouse doesn't exist"), 400
        if not pDAO.getPart(data['p_id']) or not pDAO.getPart(data['sender_p_id']):  # if part exists
            return jsonify(Error="Part doesn't exist"), 400

        sender_u_id = data['sender_u_id']
        sender_w_id = data['sender_w_id']
        sender_p_id = data['sender_p_id']
        sender_r_id = data['sender_r_id']
        receiver_r_id = data['receiver_r_id']
        receiver_quantity = data['receiver_quantity']
        t_date = data['t_date']
        t_value = data['t_value']
        t_quantity = data['t_quantity']
        u_id = data['u_id']
        w_id = data['w_id']
        p_id = data['p_id']
        #t_id = data['t_id']
        tDAO = transactionDAO()
        ##t_id = tDAO.insertTransaction(data['t_date'], data['t_value'], data['t_quantity'], data['u_id'], data['w_id'],
                                      #data['p_id'])
        if t_id and t_value and t_date and t_quantity and sender_u_id and sender_w_id and sender_p_id and sender_r_id and receiver_r_id and receiver_quantity:
            dao = ExchangeDAO()
            ExchangeDAO().updateExchange(t_id, sender_u_id, sender_w_id, sender_p_id, sender_r_id, receiver_r_id, receiver_quantity, t_date, t_value, t_quantity, u_id, w_id, p_id)
            result = self.buildExchangeAttributes(t_id, sender_u_id, sender_w_id, sender_p_id, sender_r_id,
                                                  receiver_r_id, receiver_quantity, t_date, t_value, t_quantity, u_id,
                                                  w_id, p_id)
            return jsonify(Exchange_Transactions=result), 201
        else:
            jsonify(Error="Unexpected attributes in post Request"), 400








