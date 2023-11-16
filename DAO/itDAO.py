from config.pg_config import pg_config
import psycopg2

class ITDAO:
    def __init__(self):
        connection_url = "host=localhost dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['password'])
        self.conn = psycopg2.connect(user="vbccpykujiisah",
                                     password="3e4854dbe0ce20aad8ad4cf6cd8dad1b9e2382d39f59509970541a10f30c8908",
                                     host="ec2-18-211-172-50.compute-1.amazonaws.com",
                                     port="5432",
                                     database="d50qfjb63nlom1")
    def getAllIT(self):
        cursor = self.conn.cursor()
        query = 'select it_id, t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id from incoming_transactions'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    def getIT(self, it_id):
        cursor = self.conn.cursor()
        query = 'select it_id, t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id from incoming_transactions where it_id = %s'
        cursor.execute(query, (it_id,))
        result = cursor.fetchone()
        return result
    def insertIT(self, t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id):
        cursor = self.conn.cursor()
        query = 'insert into incoming_transactions(t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id) values(%s, %s, %s,%s, %s, %s, %s, %s) returning it_id;'
        cursor.execute(query, (t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id))
        it_id = cursor.fetchone()[0]
        self.conn.commit()
        return it_id
    def updateIT(self,it_id, t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id):
        cursor = self.conn.cursor()
        query = 'update incoming_transactions set t_date = %s, t_value = %s, t_quantity = %s, s_id = %s, p_id = %s, w_id = %s, r_id = %s, u_id = %s where it_id = %s'
        cursor.execute(query, (t_date, t_value, t_quantity, s_id, p_id, w_id, r_id, u_id, it_id))
        self.conn.commit()
        return it_id