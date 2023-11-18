from config.pg_config import pg_config
import psycopg2

class warehouseDAO:
    
    def __init__(self):
        connection_url = "host=localhost dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['password'])
        self.conn = psycopg2.connect(user="vbccpykujiisah",
                                     password="3e4854dbe0ce20aad8ad4cf6cd8dad1b9e2382d39f59509970541a10f30c8908",
                                     host="ec2-18-211-172-50.compute-1.amazonaws.com",
                                     port="5432",
                                     database="d50qfjb63nlom1")
    
    def getAllWarehouses(self):
        cursor = self.conn.cursor()
        result = []
        query = "select w_id, w_name, w_location, w_budget from warehouse"
        cursor.execute(query)

        for row in cursor:
            result.append(row)
        return result
    
    def getWarehouseById(self, w_id):
        cursor = self.conn.cursor()
        query = "select w_id, w_name, w_location, w_budget from warehouse where w_id = %s"
        cursor.execute(query, (w_id,))
        result = cursor.fetchone()
        return result

    def insertWarehouse(self, w_name, w_location, w_budget):
        cursor = self.conn.cursor()
        query = "insert into warehouse(w_name, w_location, w_budget) values (%s, %s, %s) returning w_id"
        cursor.execute(query, (w_name, w_location, w_budget))
        w_id = cursor.fetchone()[0]
        self.conn.commit()
        return w_id
    
    def deleteByWarehouseId(self, w_id):
        cursor = self.conn.cursor()
        query = "delete from warehouse where w_id = %s"
        cursor.execute(query, (w_id,))
        count = cursor.rowcount
        self.conn.commit()
        return count

    def updateWarehouseById(self, w_id, w_name, w_location, w_budget):
        cursor = self.conn.cursor()
        query = "update warehouse set w_name = %s, w_location = %s, w_budget = %s where w_id = %s"
        cursor.execute(query, (w_name, w_location, w_id, w_budget))
        count = cursor.rowcount
        self.conn.commit()
        return count
    def partIn(self, w_id, p_id, r_id):
        cursor = self.conn.cursor()
        query = ("Select p_id "
                 "from warehouse natural inner join racks natural inner join parts "
                 "where p_id = %s and w_id = %s and r_id = %s")
        cursor.execute(query, (p_id, w_id, r_id))
        return cursor.fetchone() #checking if part in warehouse racks
    def partInStock(self, w_id, p_id):
        cursor = self.conn.cursor()
        query = ("Select r_id "
                 "from warehouse natural inner join racks natural inner join parts "
                 "where p_id = %s and w_id = %s")
        cursor.execute(query, (p_id, w_id))
        return cursor.fetchone()
    def getLowStock(self,w_id):
        cursor = self.conn.cursor()
        query = "Select r_id, r_amount, w_id, p_id, r_capacity from racks natural inner join warehouse where w_id=%s and r_amount < r_capacity*0.25 order by r_amount limit 5 "
        cursor.execute(query,(w_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    def getExpensive(self,w_id):
        cursor = self.conn.cursor()
        query = ("Select r_id, r_amount, w_id, p_id, r_capacity, sum(r_amount*p_price) as total_price "
                 "from racks natural inner join warehouse natural inner join parts "
                 "where w_id=%s group by r_id, r_amount, w_id, p_id, r_capacity "
                 "order by total_price desc "
                 "limit 5 ")
        cursor.execute(query,(w_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    def getBudget(self, w_id):
        cursor = self.conn.cursor()
        query = "Select w_budget from warehouse where w_id = %s"
        w_budget = cursor.execute(query, (w_id,))
        return cursor.fetchone()

    def updateBudget(self, w_id, t_value):
        cursor = self.conn.cursor()
        query = "update warehouse set w_budget = w_budget - %s where w_id = %s returning warehouse.w_budget"
        w_budget = cursor.execute(query, (t_value, w_id))
        self.conn.commit()
        return w_budget
    def addBudget(self, w_id, t_value):
        cursor = self.conn.cursor()
        query = "update warehouse set w_budget = w_budget + %s where w_id = %s returning warehouse.w_budget"
        w_budget = cursor.execute(query, (t_value, w_id))
        self.conn.commit()
        return w_budget
