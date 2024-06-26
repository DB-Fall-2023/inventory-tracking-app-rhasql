from config.pg_config import pg_config
import psycopg2

class OTDAO:
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
    def getAllOT(self):
        cursor = self.conn.cursor()
        query = 'select t_id, ot_buyername, ot_sentto, t_date, t_value, t_quantity, p_id, w_id, u_id from outgoing_transactions natural inner join transactions'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    def getOT(self, t_id):
        cursor = self.conn.cursor()
        query = 'select t_id, ot_buyername, ot_sentto, t_date, t_value, t_quantity, p_id, w_id, u_id from outgoing_transactions natural inner join transactions where t_id = %s'
        cursor.execute(query, (t_id,))
        result = cursor.fetchone()
        return result
    def insertOT(self, t_id, ot_buyername, ot_sento):
        cursor = self.conn.cursor()
        query = 'insert into outgoing_transactions(t_id, ot_buyername,ot_sentto) values(%s,%s, %s) returning t_id;'
        cursor.execute(query, (t_id, ot_buyername, ot_sento))
        it_id = cursor.fetchone()[0]
        self.conn.commit()
        return it_id
    def updateOT(self,t_id, ot_buyername, ot_sentto, t_date, t_value, t_quantity, p_id, w_id, u_id):
        cursor = self.conn.cursor()
        query = 'update transactions set t_date = %s, t_value = %s, t_quantity = %s, p_id = %s, w_id = %s, u_id = %s where t_id = %s'
        cursor.execute(query, (t_date, t_value, t_quantity, p_id, w_id, u_id, t_id))
        self.conn.commit()
        query = 'update outgoing_transactions set ot_buyername = %s, ot_sentto = %s where t_id = %s'
        cursor.execute(query, (ot_buyername, ot_sentto, t_id))
        self.conn.commit()
        return t_id