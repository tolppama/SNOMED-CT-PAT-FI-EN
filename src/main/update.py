import pandas as pd
from services import Get, Set, Database, Excel, clean_spaces
from actions import Inactivate, New, FSN, NewConcept, NewTerm, Administrative
from config import Config


class Update:
    """The main driver class for the application

    This class is responsible for orchestrating the entire application. It reads the excel and database tables,
    determines the type of updates required, and then applies the updates to the database table. Finally, it writes
    the updated database table to the excel file.
    """
    def __init__(self, password, intl=False, table=None) -> None:
        self.__intl = intl
        self.__table = table
        self.__config = Config(password)
        self.__excel = Excel(self.__config)
        self.__database = Database(self.__config)

    def __get_tables(self) -> tuple:
        """Reads the excel and database tables

        Returns:
            tuple: A tuple containing the excel and database tables in dataframes
        """
        if self.__intl:
            excel = self.__table
        else:
            excel = self.__excel.get()
        database = self.__database.get()
        return excel, database

    def __get_update_types(self, excel: 'pd.DataFrame', database: 'pd.DataFrame') -> tuple:
        """Determines the type of updates required

        Args:
            excel (pd.DataFrame): The excel containing the updates
            database (pd.DataFrame): The database table

        Returns:
            tuple: holds all the different types of updates required
        """
        edit_rows = Get.edit_rows(excel, database)
        new_rows = Get.new_rows(excel)
        fsn_rows = Get.fsn_rows(excel)
        administrative = Get.administrative_rows(excel)
        inactivated_rows = Get.inactivated_rows(excel)
        activated_rows = Get.activated_rows(excel)
        return edit_rows, new_rows, fsn_rows, administrative, inactivated_rows, activated_rows

    def run(self, progress_callback=None):
        """The main driver function for the application
        """
        excel, database = self.__get_tables()
        if progress_callback:
            progress_callback(5)
        edit_rows, new_rows, fsn_rows, administrative, inactivated_rows, activated_rows = self.__get_update_types(
            excel, database)
        if progress_callback:
            progress_callback(10)

        table = Inactivate(database, inactivated_rows, self.__config).commit()
        if progress_callback:
            progress_callback(20)
        table = FSN(table, fsn_rows).commit()
        if progress_callback:
            progress_callback(30)
        table = Administrative(table, administrative).commit()
        if progress_callback:
            progress_callback(40)
        table = New(table, new_rows, self.__config).commit()
        if progress_callback:
            progress_callback(50)
        table = NewConcept(table, edit_rows["new_concept"], self.__config).commit()
        if progress_callback:
            progress_callback(60)
        table = NewTerm(table, edit_rows["new_term"], self.__config).commit()
        if progress_callback:
            progress_callback(70)
        table = Set.empty_status_column(table)
        table = clean_spaces(table)
        if self.__intl:
            # table = table.drop(columns=['accept', 'meta'])
            print(table.columns)
            print(table)
        self.__excel.post(table)
        if progress_callback:
            progress_callback(90)
        self.__database.post(table)
        if progress_callback:
            progress_callback(100)
