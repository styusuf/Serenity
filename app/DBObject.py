import logging
import traceback


class DBObject(object):
    """Parent DB Object"""
    def __init__(self):
        self.id = -1
        self.statement = None
        self.params = None

    def update_sql_file(self, filename, conn):
        """update sql file with insert statement for this ingredient"""
        if not self.statement:
            logging.error("update_sql_file:Please populate the statement first")
            return -1
        else:
            cursor = conn.cursor()
            with open(filename, 'a') as f:
                f.write(cursor.mogrify(self.statement, self.params) + ";\n")
            cursor.close()
            logging.info("update_sql_file: Updated {} with SQL statement".format(filename))
            return 0


    def populate_from_db(self, conn, obj_id):
        """Update the object from the database cursor and id"""
        pass

    def update_db(self, conn):
        """update the database"""
        if not self.statement:
            logging.error("update_db:Please populate the statement first")
            return -1
        cursor = conn.cursor()
        try:
            cursor.execute(self.statement, self.params)
        except:
            e = traceback.format_exc(5)
            logging.error(e)
            return -1
        cursor.close()
        return 0
