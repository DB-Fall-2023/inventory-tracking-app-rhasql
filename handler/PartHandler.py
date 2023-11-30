#WILL CONTINUE TO COMMENT CODE LATER
from flask import jsonify
from DAO.partsDAO import PartsDAO
from matplotlib import pyplot as plt
class PartHandler:

    # Costructs dictionary of attributes
    def mapToDict(self,t):
        result = {}
        result['p_id'] = t[0]
        result['p_name'] = t[1]
        result['p_price'] = t[2]
        result['p_type'] = t[3]
        result['p_color'] = t[4]
        result['p_weight'] = t[5]
        return result

   #Costructs dictionary of attributes
    def build_part_attributes(self, p_id, p_name, p_price, p_type, p_color, p_weight):
        result = {}
        result['p_id'] = p_id
        result['p_name'] = p_name
        result['p_price'] = p_price
        result['p_type'] = p_type
        result['p_color'] = p_color
        result['p_weight'] = p_weight
        return result

    def buildPprice(self, data):
        result = {}
        result['p_name'] = data[0]
        result['p_price'] = data[1]
        return result

    #Gets all parts in parts table
    def getAllParts(self):
        dao = PartsDAO()
        dtuples = dao.getAllParts()
        result = []
        for x in dtuples:
            result.append(self.mapToDict(x))
        return jsonify(result)

    #Adds part to DB
    def addPart(self, json):
        if len(json) != 5:
            return jsonify(Error="Malformed request"), 400
        # Sets variables to send to build_part_attributes function
        p_name = json['p_name']
        p_price = json['p_price']
        p_type = json['p_type']
        p_color = json['p_color']
        p_weight = json['p_weight']
        # Checks if any are NULL
        if len(json) != 5:
            return jsonify(Error="Malformed request"), 400
        if p_name and p_price and p_type and p_color and p_weight:
            dao = PartsDAO()
            p_id = dao.insert(p_name, p_price, p_type, p_color, p_weight)
            result = self.build_part_attributes(p_id, p_name, p_price, p_type, p_color, p_weight)
            return jsonify(Part=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    #Gets single part (according to id)
    def getPart(self, p_id):
        dao = PartsDAO()
        dtuple = dao.getPart(p_id)
        if not dtuple:
            return jsonify(Error="Part doesn't exist"), 404
        part = self.mapToDict(dtuple)
        return jsonify(Part=part)

    #Updates part (according to id)
    def updatePart(self, p_id, json):
        dao = PartsDAO()
        #Checks if part exists in DB
        #Returns an error if it doesn't
        if not dao.getPart(p_id):
            return jsonify(Error="Part doesn't exist"), 404
        else:
            #Catches any updates that dont have all 5 attributes (exclusing p_id)
            if(len(json) != 5):
                return jsonify(Error="Improperly constructed request"), 400
        #Sets variables to send to build_part_attributes function
        p_name = json['p_name']
        p_price = json['p_price']
        p_type = json['p_type']
        p_color = json['p_color']
        p_weight = json['p_weight']
        #Checks if any are NULL
        if p_name and p_price and p_type and p_color and p_weight:
            dao.update(p_id,p_name, p_price, p_type, p_color, p_weight)
            result = self.build_part_attributes(p_id, p_name, p_price, p_type, p_color, p_weight)
            return jsonify(Part=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400
    def deletePart(self, p_id):
        dao = PartsDAO()
        if not dao.getPart(p_id):
            return jsonify(Error="Part doesn't exist"), 404
        else:
            p_id = dao.deletePart(p_id)
            return jsonify(DeleteStatus = "OK"), 200

    def getPrice(self):
        dao = PartsDAO()
        ppJson = dao.getPrice()
        pName = []
        pPrice = []
        result = []
        for x in ppJson:
            result.append(PartHandler().buildPprice(x))
        for y in result:
            pName.append(y['p_name'])
            pPrice.append(y['p_price'])
        plt.bar(range(0, len(pPrice)), pPrice)
        plt.xticks(range(0, len(pName)), pName)
        plt.show()
        return jsonify(result)