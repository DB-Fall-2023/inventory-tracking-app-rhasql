from config.pg_config import pg_config
import psycopg2

class UserDAO:
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


    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = 'select u_id, fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id from wUser;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserById(self, u_id):
        cursor = self.conn.cursor()
        query = 'select u_id, fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id from wUser where u_id = %s'
        cursor.execute(query,(u_id,))
        result = cursor.fetchone()
        return result


    def add(self,fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id):
        cursor = self.conn.cursor()
        query = 'insert into wUser(fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id) values (%s, %s, %s, %s, %s, %s, %s, %s) returning u_id'
        cursor.execute(query, (fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id))
        u_id = cursor.fetchone()[0]
        self.conn.commit()
        return u_id

    def updateUser(self,u_id, fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id):
        cursor = self.conn.cursor()
        query = 'update wUser set fname = %s, lname = %s, b_date = %s, u_password = %s, u_salary = %s, u_address = %s, u_SSN = %s, w_id = %s where u_id = %s'
        cursor.execute(query, (fname, lname, b_date, u_password, u_salary, u_address, u_SSN, w_id, u_id))
        self.conn.commit()
        return u_id

    def deleteUser(self, u_id):
        cursor = self.conn.cursor()
        query = 'delete from wUser where u_id = %s'
        cursor.execute(query, (u_id,))
        self.conn.commit()
        return u_id
    def inWarehouse(self, u_id, w_id):
        cursor = self.conn.cursor()
        query = 'Select u_id from wuser natural inner join warehouse where u_id = %s and w_id = %s'
        cursor.execute(query, (u_id, w_id))
        return cursor.fetchone()

    def getMostUserTransactions(self):
        cursor = self.conn.cursor()
        query = ('Select u_id, count(*) '
                 'from transactions '
                 'group by u_id '
                 'order by count(*) desc '
                 'LIMIT 3')
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result