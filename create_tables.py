import psycopg2
from createTablesAndViews import cde

class Create():
    """
    ## Create Tables and Views
    - Creates tables and views with prefilled values
    - Database is hosted in heroku
    """
    def __init__(self,db_string):
        """Constructor

        Arguments:
            db_string {str} -- Database connection string
        """
        self.db_string = db_string
        self.createDb()

    def createDb(self):
        conn = psycopg2.connect(self.db_string)
        cursor = conn.cursor()

        for statement in cde:
            cursor.execute(statement)
            conn.commit()
        
        conn.close()


"""Unit Testing"""
if __name__ == '__main__':
    Create("postgres://rusejngmnnumvu:83b2d665130d7a045159ff6187d8232470c431cbe8aef1b134d19373b503645d@ec2-54-87-112-29.compute-1.amazonaws.com:5432/d2usd2salsuu27")