from flask import jsonify
from DAO.userDAO import UserDAO
from DAO.warehouseDAO import  warehouseDAO


class UserHandler:


    def build_user(self,row):
        result = {}
        result['u_id'] = row[0]
        result['fname'] = row[1]
        result['lname'] = row[2]
        result['b_date'] = row[3]
        result['u_password'] = row[4]
        result['u_salary'] = row[5]
        result['u_address'] = row[6]
        result['u_SSN'] = row[7]
        result['w_id'] = row[8]
        return result

    def build_user_attributes(self, u_id, fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id):
        result = {}
        result['u_id'] = u_id
        result['fname'] = fname
        result['lname'] = lname
        result['b_date'] = b_date
        result['u_password'] = u_password
        result['u_salary'] = u_salary
        result['u_address'] = u_address
        result['u_SSN'] = u_SSN
        result['w_id'] = w_id
        return result

    def buildMostUserTransactions(self, data):
        result = {}
        result['u_id'] = data[0]
        result['Amount of Transactions'] = data[1]
        return result

    def getAllUsers(self):
        dao = UserDAO()
        user_list = dao.getAllUsers()
        result_list = []
        for row in user_list:
            result = self.build_user(row)
            result_list.append(result)
        return jsonify(wUsers=result_list)

    def getUserById(self, u_id):
        dao = UserDAO()
        row = dao.getUserById(u_id)
        if not row:
            return jsonify(Error = 'User not found'), 404
        else:
            user = self.build_user(row)
            return jsonify(wUser = user)

    def addUser(self, form):
        wDAO = warehouseDAO()
        if len(form) != 8:
            return jsonify(Error = "Malformed Post Request"), 400
        else:
            fname = form['fname']
            lname = form['lname']
            b_date = form['b_date']
            u_password = form['u_password']
            u_salary = form['u_salary']
            u_address = form['u_address']
            u_SSN = form['u_SSN']
            if not wDAO.getWarehouseById(form['w_id']):  # if warehouse exist
                return jsonify(Error="Warehouse doesn't exist"), 400
            w_id = form['w_id']
            if fname and lname and b_date and u_password and u_salary and u_address and u_SSN and w_id:
                dao = UserDAO()
                u_id = dao.add(fname,lname,b_date,u_password,u_salary,u_address,u_SSN, w_id)
                result = self.build_user_attributes(u_id, fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id)
                return jsonify(wUsers=result), 201
            else:
                return jsonify(Error='Unexpected attributes in post request'), 400


    def updateUser(self, u_id, form):
        dao = UserDAO()
        wDAO = warehouseDAO()
        if not dao.getUserById(u_id):
            return jsonify(Error = "User not found."), 404
        else:
            if len(form) != 8:
                print(len(form))
                return jsonify(Error = "Malformed update request."), 400
            else:
                fname = form['fname']
                lname = form['lname']
                b_date = form['b_date']
                u_password = form['u_password']
                u_salary = form['u_salary']
                u_address = form['u_address']
                u_SSN = form['u_SSN']
                if not wDAO.getWarehouseById(form['w_id']):  # if warehouse exist
                    return jsonify(Error="Warehouse doesn't exist"), 400
                w_id = form['w_id']
                if fname and lname and b_date and u_password and u_salary and u_address and u_SSN and w_id:
                    dao.updateUser(u_id, fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id)
                    result = self.build_user_attributes(u_id, fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id)
                    return jsonify(wUser = result), 200
                else:
                    return jsonify(Error = 'Unexpected attributes in update request'), 400


    def deleteUser(self, u_id):
        dao = UserDAO()
        if not dao.getUserById(u_id):
            return jsonify(Error = 'User not found.'), 404
        else:
            dao.deleteUser(u_id)
            return jsonify(DeleteStatus = 'Succesful')

    def getMostUserTransactions(self):
        dao = UserDAO()
        user_list = dao.getMostUserTransactions()
        result_list = []
        for row in user_list:
            result = self.buildMostUserTransactions(row)
            result_list.append(result)
        return jsonify(UsersWithMostTransactions=result_list)

