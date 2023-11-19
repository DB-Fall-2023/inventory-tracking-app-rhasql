from config.pg_config import pg_config
import psycopg2

class SuppliersDAO:

    def __init__(self):
        connection_url = "user=%s password=%s host=%s port=%s dbname=%s" % (pg_config['user'],
                                                                            pg_config['password'],
                                                                            pg_config['host'],
                                                                            pg_config['port'],
                                                                            pg_config['dbname'])
        # self.conn = psycopg2.connect(user="vbccpykujiisah",
        #                            password="3e4854dbe0ce20aad8ad4cf6cd8dad1b9e2382d39f59509970541a10f30c8908",
        #                           host="ec2-18-211-172-50.compute-1.amazonaws.com",
        #                          port="5432",
        #                         database="d50qfjb63nlom1")
        self.conn = psycopg2.connect(connection_url)

    def getAllSuppliers(self):
        cursor = self.conn.cursor()
        result = []
        query = "select s_id, s_name, s_city, s_phone from supplier"
        cursor.execute(query)

        for row in cursor:
            result.append(row)

        return result

    def searchById(self, s_id):
        cursor = self.conn.cursor()
        query = "select s_id, s_name, s_city, s_phone from supplier where s_id = %s"
        cursor.execute(query, (s_id,))
        result = cursor.fetchone()
        return result

    def insertSupplier(self, name, city, phone):
        cursor = self.conn.cursor()
        query = "insert into supplier(s_name, s_city, s_phone) values (%s, %s, %s) returning s_id"
        cursor.execute(query, (name, city, phone,))
        sid = cursor.fetchone()[0]
        self.conn.commit()
        return sid

    def deleteById(self, s_id):
        cursor = self.conn.cursor()
        query = "delete from supplier where s_id = %s"
        cursor.execute(query, (s_id,))
        count = cursor.rowcount
        self.conn.commit()
        return count

    def updateById(self, s_id, s_name, s_city, s_phone):
        cursor = self.conn.cursor()
        query = "update supplier set s_name = %s, s_city = %s, s_phone = %s where s_id = %s"
        cursor.execute(query, (s_name, s_city, s_phone, s_id,))
        count = cursor.rowcount
        self.conn.commit()
        return count
