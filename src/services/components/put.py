import pandas as pd
from config import COLUMNS
from .get import Get


class Put:
    """Handles the updating of the database

    Put methods are used to update existing rows in the database.
    """
    @staticmethod
    def inactivate_row(code_id: int, database: 'pd.DataFrame', expiring_date: str, inaktivoinnin_selite: str, edit_comment: str, korvaava_koodi="") -> 'pd.DataFrame':
        """Inactivates a row in the database

        Args:
            code_id (int): The code id of the row to be inactivated
            database (pd.DataFrame): The database
            expiring_date (str): The determined expiring date. This value is set in the 
                                    config file and defined in the environment variables.
            inaktivoinnin_selite (str): The reason for inactivation, copied from the excel table.
            edit_comment (str): The edit comment, copied from the excel table.
            korvaava_koodi (str, optional): It is possible to just inactivate a row without replacemen,
                                            but in the case we have replacement, you can define it here. Defaults to "".

        Returns:
            pd.DataFrame: The updated database
        """

        index = Get.index_by_codeid(database, code_id)
        database.loc[index, COLUMNS["active"]] = "N"
        database.loc[index, COLUMNS["expiring_date"]] = expiring_date
        database.loc[index, COLUMNS["inaktivoinnin_selite"]
                     ] = inaktivoinnin_selite
        database.loc[index, COLUMNS["edit_comment"]] = edit_comment
        database.loc[index, COLUMNS["korvaava_koodi"]] = korvaava_koodi
        return database

    @staticmethod
    def activate_row(code_id: int, database: 'pd.DataFrame', beginning_date: str, expiring_date: str, edit_comment: str) -> 'pd.DataFrame':
        """Activates a row in the database

        Not used at the moment, but could be used in the future.

        Args:
            code_id (int): The code id of the row to be activated
            database (pd.DataFrame): The database
            beginning_date (str): The determined beginning date. This value is set in the
                                    config file and defined in the environment variables.
            expiring_date (str): The determined expiring date. This value is set in the
                                    config file and defined in the environment variables.
            edit_comment (str): The edit comment, copied from the excel table.

        Returns:
            pd.DataFrame: The updated database
        """

        index = Get.index_by_codeid(database, code_id)
        database.loc[index, COLUMNS["active"]] = "Y"
        database.loc[index, COLUMNS["beginning_date"]] = beginning_date
        database.loc[index, COLUMNS["expiring_date"]] = expiring_date
        database.loc[index, COLUMNS["inaktivoinnin_selite"]] = None
        database.loc[index, COLUMNS["edit_comment"]] = edit_comment
        return database

    @staticmethod
    def fsn(code_id: int, database: 'pd.DataFrame', new_fsn: str) -> 'pd.DataFrame':
        """Updates the fully specified name of a row in the database

        Args:
            code_id (int): The code id of the row to be updated
            database (pd.DataFrame): The database
            new_fsn (str): The new fully specified name

        Returns:
            pd.DataFrame: The updated database
        """

        index = Get.index_by_codeid(database, code_id)
        database.loc[index, COLUMNS["concept_fsn"]] = new_fsn
        return database

    @staticmethod
    def administrative_columns(code_id: int, database: 'pd.DataFrame', en_row: 'pd.Series', administrative_columns: list[str]) -> 'pd.DataFrame':
        """Updates the administrative columns of a row in the database

        The columns are defined in the administrative action class.
        These columns are not visible to the end-users and are for internal use only.

        Args:
            code_id (int): The code id of the row to be updated
            database (pd.DataFrame): The database
            en_row (pd.Series): The en row
            administrative_columns (list[str]): The list of administrative columns to be updated

        Returns:
            pd.DataFrame: The updated database
        """
        index = Get.index_by_codeid(database, code_id)
        for column in administrative_columns:
            database.loc[index, column] = en_row[column]
        return database
    
    @staticmethod
    def lang_row_en_row_code_id(code_id: int, database: 'pd.DataFrame', en_row_code_id: int) -> 'pd.DataFrame':
        """Updates the en row code id of a lang row in the database

        Args:
            code_id (int): The code id of the row to be updated
            database (pd.DataFrame): The database
            en_row_code_id (int): The en row code id

        Returns:
            pd.DataFrame: The updated database
        """
        index = Get.index_by_codeid(database, code_id)
        database.loc[index, COLUMNS["en_row_code_id"]] = en_row_code_id
        return database
    

    @staticmethod
    def lang_row_en_row_code_id_with_beginning_date(code_id: int, database: 'pd.DataFrame', en_row_code_id: int, beginning_date: str) -> 'pd.DataFrame':
        """Updates the en row code id and beginning date of a lang row in the database

        Args:
            code_id (int): The code id of the row to be updated
            database (pd.DataFrame): The database
            en_row_code_id (int): The en row code id
            beginning_date (str): The new beginning date

        Returns:
            pd.DataFrame: The updated database
        """
        index = Get.index_by_codeid(database, code_id)
        database.loc[index, COLUMNS["en_row_code_id"]] = en_row_code_id
        database.loc[index, COLUMNS["beginning_date"]] = beginning_date
        return database
