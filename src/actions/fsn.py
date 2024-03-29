import pandas as pd
from config import COLUMNS
from services.components import Put


class FSN:
    """Class for updating the FSN

    This class is used to update the FSN in the database.
    It takes the database and the FSN rows as input and updates the FSN in the database.
    It updates the FSN of all the rows with same concept_id.
    """

    def __init__(self, database: 'pd.DataFrame', fsn_edit_en_rows: 'pd.DataFrame', new: bool = False):
        self.__database = database
        self.__fsn_edit_en_rows = fsn_edit_en_rows
        self.__new = new

    def __update_fsn(self, en_row: 'pd.Series'):
        """Updates the FSN in the database

        Take the concept_id from the en row and updates all the rows in the database that have
        the same concept_id.

        Args:
            en_row (pd.Series): The target concepts to be updated
        """
        if self.__new:
            concept_id = en_row[COLUMNS["concept_id"]]
        else:
            concept_id = self.__database[self.__database[COLUMNS["code_id"]] == en_row[COLUMNS["code_id"]]][COLUMNS["concept_id"]].values[0]
        concept_rows = self.__database[self.__database[COLUMNS["concept_id"]]
                                       == concept_id]
        for _, concept_row in concept_rows.iterrows():
            self.__database = Put.fsn(
                concept_row[COLUMNS["code_id"]], self.__database, en_row[COLUMNS["concept_fsn"]])
        if not self.__new:
            self.__database = Put.fsn(
                en_row[COLUMNS["code_id"]], self.__database, en_row[COLUMNS["concept_fsn"]])

    def commit(self):
        """Main function for updating the FSN
        """

        for _, en_row in self.__fsn_edit_en_rows.iterrows():
            self.__update_fsn(en_row)
        return self.__database
