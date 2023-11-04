from config.pg_config import pg_config
import psycopg2

class UserDAO:
    def __init__(self):
        connection_url = "host=localhost dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['password'])
        self.conn = psycopg2.connect(user="vbccpykujiisah",
                                     password="3e4854dbe0ce20aad8ad4cf6cd8dad1b9e2382d39f59509970541a10f30c8908",
                                     host="ec2-18-211-172-50.compute-1.amazonaws.com",
                                     port="5432",
                                     database="d50qfjb63nlom1")


    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = 'select u_id, fname, lname, b_date, u_password, u_salary, u_address, u_SSN from wUser;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def add(self,fname, lname, b_date, u_password, u_salary, u_address, u_SSN):
        cursor = self.conn.cursor()
        query = 'insert into wUser(fname, lname, b_date, u_password, u_salary, u_address, u_SSN) values (%s, %s, %s, %s, %s, %s, %s) returning u_id'
        cursor.execute(query, (fname, lname, b_date, u_password, u_salary, u_address, u_SSN))
        u_id = cursor.fetchone()[0]
        self.conn.commit()
        return u_id
