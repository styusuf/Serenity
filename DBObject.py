import logging
import traceback


class DBObject(object):
    """Parent DB Object"""
    def __init__(self):
        self.id = -1
        self.statement = None

    def update_sql_file(self, filename):
        """update sql file with insert statement for this ingredient"""
        if not self.statement:
            logging.error("update_sql_file:Please populate the statement first")
            return -1
        else:
            with open(filename, 'a') as f:
                f.write(self.statement + ";\n")
            logging.info("update_sql_file: Updated {} with SQL statement".format(filename))

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
            cursor.execute(self.statement)
        except:
            e = traceback.format_exc()
            logging.error(e)
            return -1
        conn.commit()
        cursor.close()
        return 0
