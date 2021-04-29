import psycopg2
from tabulate import tabulate


class GetStats():
    """
    ## Get Statistics
    Gets various statistics from the Databse such as:
    - Count of covid infected people
    - Number of hospital beds available
    - Hospital equipment statistics
    - Average cost to patient
    - Health statitics
    - Severity statistics
    """
    __conn: psycopg2._ext.connection = None
    __cursor: psycopg2._ext.cursor = None

    def __init__(self,db_string):
        """Constructor

        Arguments:
            db_string {str} -- Database connection string
        """
        self.db_string = db_string
        self.__conn = psycopg2.connect(self.db_string)
        self.__cursor = self.__conn.cursor()


    def get_hospital_details(self):
        """
        Get the various details of hospitals

        Prints a tabular format of hospital details
        """

        self.__cursor.execute("""
        SELECT hospital_name, hospital_details, capacity FROM hospitals WHERE is_covid_dedicated = TRUE ORDER BY capacity DESC;
        """)
        headers = [desc[0] for desc in self.__cursor.description]
        print('\n\n\n',tabulate(self.__cursor.fetchall(), headers = headers),'\n\n')


    def get_empty_beds(self):
        """
        Get the count of empty beds in each hospital.

        Prints a tabular format of hospital name and number empty beds
        """

        self.__cursor.execute("""
        SELECT a.hospital_name,
            a.capacity - b.count as empty_beds
        FROM hospitals a JOIN (SELECT hospital_id,COUNT(*) FROM patient_hospital_details WHERE discharge_date IS NULL GROUP BY hospital_id) b ON a.hospital_id = b.hospital_id
        ;
        """)
        headers = [desc[0] for desc in self.__cursor.description]
        print('\n\n\n',tabulate(self.__cursor.fetchall(), headers = headers), '\n\n')


    def get_total_discharged(self):
        """
        Get the count of discarged patients

        Prints the number of discarged patients
        """

        self.__cursor.execute("""
        SELECT COUNT(*) FROM patient_hospital_details WHERE discharge_date IS NULL
        ;
        """)
        print('Total Discharged -------', self.__cursor.fetchone()[0],'\n\n')


    def get_severe_cases_count(self):
        """
        Get the count of severe cases

        Prints the number of severe cases
        """
        self.__cursor.execute("""
        SELECT COUNT(*) FROM patient_hospitals WHERE severity_id = 1;
        """)
        print('Total Severe Cases -------', self.__cursor.fetchone()[0],'\n\n')


    def get_hospital_items(self):
        """
        Get the available hospital items of a hospital
        """

        print("Select a hopital number")
        self.__cursor.execute("""
        SELECT DISTINCT a.hospital_id,b.hospital_name FROM hospital_items a JOIN hospitals b ON a.hospital_id=b.hospital_id ORDER BY a.hospital_id;
        """)
        print(tabulate(self.__cursor.fetchall(), headers = ['number','name']), )
        try:
            number = int(input("Enter a number: ")) 
        except:
            print("invalid number... 1 assumed")
            number = 1
        
        self.__cursor.execute("""
            SELECT equiment_name,quality,quantity FROM hospital_items WHERE hospital_id = {};
        """.format(number))

        headers = [desc[0] for desc in self.__cursor.description]
        print('\n\n\n',tabulate(self.__cursor.fetchall(), headers = ['equiment','desc','quantity']),'\n\n')
        

"""Unit Testing"""
if __name__ == '__main__':
    stats = GetStats("postgres://rusejngmnnumvu:83b2d665130d7a045159ff6187d8232470c431cbe8aef1b134d19373b503645d@ec2-54-87-112-29.compute-1.amazonaws.com:5432/d2usd2salsuu27")   
    stats.get_hospital_details()
    stats.get_empty_beds()
    stats.get_total_discharged()
    stats.get_severe_cases_count()
    stats.get_hospital_items()