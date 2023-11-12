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
        query = "select w_id, w_name, w_location from warehouse"
        cursor.execute(query)

        for row in cursor:
            result.append(row)
        return result
    
    def getWarehouseById(self, w_id):
        cursor = self.conn.cursor()
        query = "select w_id, w_name, w_location from warehouse where w_id = %s"
        cursor.execute(query, (w_id,))
        result = cursor.fetchone()
        return result

    def insertWarehouse(self, w_name, w_location):
        cursor = self.conn.cursor()
        query = "insert into warehouse(w_name, w_location) values (%s, %s) returning w_id"
        cursor.execute(query, (w_name, w_location,))
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

    def updateWarehouseById(self, w_id, w_name, w_location):
        cursor = self.conn.cursor()
        query = "update warehouse set w_name = %s, w_location = %s where w_id = %s"
        cursor.execute(query, (w_name, w_location, w_id,))
        count = cursor.rowcount
        self.conn.commit()
        return count
