from config.pg_config import pg_config
import psycopg2

class transactionDAO:
    def __init__(self):
        connection_url = "host=localhost dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['password'])
        self.conn = psycopg2.connect(user="vbccpykujiisah",
                                     password="3e4854dbe0ce20aad8ad4cf6cd8dad1b9e2382d39f59509970541a10f30c8908",
                                     host="ec2-18-211-172-50.compute-1.amazonaws.com",
                                     port="5432",
                                     database="d50qfjb63nlom1")

    def insertTransaction(self, t_date, t_value, t_quantity):
        cursor = self.conn.cursor()
        query = 'insert into transactions(t_date,t_value,t_quantity) values(%s,%s,%s) returning transactions.t_id'
        cursor.execute(query,(t_date, t_value, t_quantity))
        t_id = cursor.fetchone()[0]
        self.conn.commit()
        return t_id