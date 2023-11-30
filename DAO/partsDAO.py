from config.pg_config import pg_config
import psycopg2
class PartsDAO:
    def __init__(self):
        connection_url = "user=%s password=%s host=%s port=%s dbname=%s" % (pg_config['user'],
                                                            pg_config['password'],
                                                            pg_config['host'],
                                                            pg_config['port'],
                                                            pg_config['dbname'])
        #self.conn = psycopg2.connect(user="vbccpykujiisah",
         #                            password="3e4854dbe0ce20aad8ad4cf6cd8dad1b9e2382d39f59509970541a10f30c8908",
          #                           host="ec2-18-211-172-50.compute-1.amazonaws.com",
           #                          port="5432",
            #                         database="d50qfjb63nlom1")
        self.conn = psycopg2.connect(connection_url)
    def getAllParts(self):
        cursor = self.conn.cursor()
        result = []
        query = "select p_id, p_name, p_price, p_type, p_color, p_weight from parts"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result
    def insert(self, p_name, p_price, p_type, p_color, p_weight):
        cursor = self.conn.cursor()
        query ="insert into parts(p_name, p_price, p_type, p_color, p_weight) values (%s, %s, %s, %s, %s) returning parts.p_id;"
        cursor.execute(query, (p_name, p_price, p_type, p_color, p_weight,))
        self.conn.commit()
        p_id = cursor.fetchone()[0]
        return p_id
    def getPart(self, p_id):
        cursor = self.conn.cursor()
        query = "Select p_id, p_name, p_price, p_type, p_color, p_weight From parts where p_id =%s;"
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        return result
    def update(self,p_id, p_name, p_price, p_type, p_color, p_weight):
        cursor = self.conn.cursor()
        query = "update parts set p_name = %s, p_price = %s, p_type = %s, p_color = %s, p_weight = %s where p_id = %s;"
        cursor.execute(query, (p_name,p_price, p_type, p_color, p_weight, p_id,))
        self.conn.commit()
        return p_id
    def deletePart(self, p_id):
        cursor =  self.conn.cursor()
        query = "delete from parts where p_id = %s"
        cursor.execute(query,(p_id,))
        self.conn.commit()
        return p_id
    def getPrice(self):
        cursor = self.conn.cursor()
        query = ("Select p_name, p_price "
                 "From parts")
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result