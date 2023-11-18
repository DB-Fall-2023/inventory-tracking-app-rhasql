from config.pg_config import pg_config
import psycopg2

class SuppliesDAO:
    def __init__(self):
        connection_url = "host=localhost dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['password'])
        self.conn = psycopg2.connect(user="vbccpykujiisah",
                                     password="3e4854dbe0ce20aad8ad4cf6cd8dad1b9e2382d39f59509970541a10f30c8908",
                                     host="ec2-18-211-172-50.compute-1.amazonaws.com",
                                     port="5432",
                                     database="d50qfjb63nlom1")

    def getAllSupplies(self):
        cursor = self.conn.cursor()
        result = []
        query = "select p_id, s_id, stock from supplies;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result
    def insertSupplies(self, p_id, s_id, stock):
        cursor = self.conn.cursor()
        query ="insert into supplies(p_id, s_id, stock) values (%s, %s, %s) returning supplies.p_id, supplies.s_id;"
        cursor.execute(query, (p_id, s_id, stock,))
        self.conn.commit()
        #p_id = cursor.fetchone()[0]
        return p_id, s_id
    def getSupplies(self, p_id, s_id):
        cursor = self.conn.cursor()
        query = "select p_id, s_id, stock from supplies where p_id=%s and s_id=%s;"
        cursor.execute(query,(p_id, s_id,))
        result = cursor.fetchone()
        return result
    def updateSupplies(self, p_id, s_id, stock):
        cursor = self.conn.cursor()
        query = "update supplies set stock = %s where p_id = %s and s_id = %s;"
        cursor.execute(query,(stock, p_id, s_id))
        self.conn.commit()
        return p_id, s_id
    def deleteSupplies(self, p_id, s_id):
        cursor = self.conn.cursor()
        query = "delete from supplies where p_id = %s and s_id = %s"
        cursor.execute(query, (p_id, s_id))
        self.conn.commit()
        return p_id, s_id

    def supplies(self, p_id, s_id):
        cursor = self.conn.cursor()
        query = "Select p_id from supplies where p_id = %s and s_id = %s"
        cursor.execute(query, (p_id, s_id))
        return cursor.fetchone()
