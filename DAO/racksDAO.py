from config.pg_config import pg_config
import psycopg2

class RacksDao:
    def __init__(self):
        connection_url = "host=localhost dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['password'])
        self.conn = psycopg2.connect(user="vbccpykujiisah",
                                     password="3e4854dbe0ce20aad8ad4cf6cd8dad1b9e2382d39f59509970541a10f30c8908",
                                     host="ec2-18-211-172-50.compute-1.amazonaws.com",
                                     port="5432",
                                     database="d50qfjb63nlom1")

    def getAllRacks(self):
        cursor = self.conn.cursor()
        query = 'select r_id, r_capacity, r_fullCost, r_partsinstock from racks'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRacksById(self, r_id):
        cursor = self.conn.cursor()
        query = 'select r_id, r_capacity, r_fullCost, r_partsinstock from racks where r_id = %s'
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        return result

    def insertRack(self, r_capacity, r_fullCost, r_partsinstock):
        cursor = self.conn.cursor()
        query = 'insert into racks(r_capacity, r_fullCost, r_partsinstock) values(%s, %s, %s) returning racks.r_id;'
        cursor.execute(query, (r_capacity, r_fullCost, r_partsinstock,))
        r_id = cursor.fetchone()[0]
        self.conn.commit()
        return r_id

    def updateRack(self, r_id, r_capacity, r_fullcost, r_partsinstock):
        cursor = self.conn.cursor()
        query = 'update racks set r_capacity = %s, r_fullcost = %s, r_partsinstock = %s where r_id = %s'
        cursor.execute(query, (r_capacity, r_fullcost, r_partsinstock,r_id,))
        self.conn.commit()
        return r_id

    def deleteRack(self, r_id):
        cursor = self.conn.cursor()
        query = 'delete from racks where r_id = %s'
        cursor.execute(query, (r_id,))
        self.conn.commit()
        return r_id