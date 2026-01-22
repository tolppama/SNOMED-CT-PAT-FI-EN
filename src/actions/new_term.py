import pandas as pd
from config import COLUMNS, ADMINISTRATIVE_COLUMNS
from services import Get, Put, Set, Post, Verhoeff
from .fsn import FSN


class NewTerm:
    """Class for editing terms

    This class is used to edit terms in the database.
    It takes the database, the new term rows and the configuration as input and edits the terms
    accordingly in the database.

    It inactivates the old term and creates a new term with the new values.

    Does not handle concept changes, only term changes.

    Can be used to set new intl or national termids for terms that have changed.
    """

    def __init__(self, database: 'pd.DataFrame', new_term_en_rows: 'list', config: object) -> None:
        self.__database = database
        self.__new_term_en_rows = new_term_en_rows
        self.__verhoeff = Verhoeff()
        self.__config = config

    def __set_en_row(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series') -> 'pd.Series':
        """Updates the en row for the new term

        Inactivates the old en row and creates a new en row with the new values.
        If the new term row has no term id, it generates a national new term id.
        On the other hand, if the new term row has a term id, it takes that
        and copies it to the new term rows.

        Args:
            new_en_row (pd.Series): The en row of the new term
            old_en_row (pd.Series): The old en row from the database

        Returns:
            pd.Series: The new en row
        """

        new_en_row = Set.en_row_code_id(new_en_row, self.__database)
        new_en_row = Set.date(new_en_row, self.__config)
        new_en_row = Set.administrative(new_en_row, old_en_row, self.__config)
        new_en_row = Set.term_id(new_en_row, old_en_row,
                                 self.__database, self.__verhoeff, self.__config)
        # set the concept id columns from the old en row
        new_en_row[COLUMNS["concept_id"]] = old_en_row[COLUMNS["concept_id"]]
        new_en_row[COLUMNS["legacy_concept_id"]
                   ] = old_en_row[COLUMNS["legacy_concept_id"]]
        # set the FSN columns from the old en row if new row has no FSN
        new_en_row = Set.fsn(new_en_row, old_en_row, self.__config)
        self.__database = FSN(
            self.__database, new_en_row.to_frame().transpose(), True).commit()
        # inactivate the old en row
        self.__database = Put.inactivate_row(old_en_row[COLUMNS["code_id"]], self.__database, self.__config.version_date,
                                             old_en_row[COLUMNS["inaktivoinnin_selite"]], old_en_row[COLUMNS["edit_comment"]], new_en_row[COLUMNS["code_id"]])
        self.__database = Post.new_row_to_database_table(
            new_en_row, self.__database)
        return new_en_row

    def __set_lang_rows(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series') -> None:
        """Updates the lang rows using the new en row

        Inactivates the old lang rows and creates new lang rows with the new values.
        If the old lang row term id is the same as the old en row term id,
        it sets the new lang row term and term ids to the new en row term ids.
        If they are not the same, it gets the SN2 from the new en row and sets the new lang row term id.

        Args:
            new_en_row (pd.Series): The new en row
            old_en_row (pd.Series): The old en row from the database
        """

        old_lang_rows = Get.lang_rows_by_en(self.__database, old_en_row)
        for _, old_lang_row in old_lang_rows.iterrows():
            # check if the old lang row term id is the same as the old en row term id
            # if it is, set the new lang row term and term ids to the new en row term ids
            if old_lang_row[COLUMNS["legacy_term_id"]] == old_en_row[COLUMNS["legacy_term_id"]]:
                new_lang_row = old_lang_row.copy()
                new_lang_row[COLUMNS["code_id"]
                             ] = Get.next_codeid(self.__database)
                new_lang_row = Set.lang_row_concept_columns(
                    new_lang_row, new_en_row)
                new_lang_row = Set.lang_administrative(
                    new_en_row, new_lang_row, ADMINISTRATIVE_COLUMNS)

                new_lang_row[COLUMNS["legacy_term_id"]
                             ] = new_en_row[COLUMNS["legacy_term_id"]]
                new_lang_row[COLUMNS["term_id"]
                             ] = new_en_row[COLUMNS["term_id"]]
                new_lang_row[COLUMNS["term"]] = new_en_row[COLUMNS["term"]]
                new_lang_row = Set.date(new_lang_row, self.__config)
                # inactivate the old lang row
                self.__database = Put.inactivate_row(old_lang_row[COLUMNS["code_id"]], self.__database, self.__config.version_date,
                                                     old_en_row[COLUMNS["inaktivoinnin_selite"]], old_en_row[COLUMNS["edit_comment"]], new_lang_row[COLUMNS["code_id"]])
                # add the new lang row to the database
                self.__database = Post.new_row_to_database_table(
                    new_lang_row, self.__database)
            else:
                # if the old lang row term id is not the same as the old en row term id
                # change only the COLUMNS["en_row_code_id"] = new_en_row code_id
                # self.__database = Put.lang_row_en_row_code_id(
                #    old_lang_row[COLUMNS["code_id"]], self.__database, new_en_row[COLUMNS["code_id"]])
                # and update the beginning date to match the new en row
                #self.__database = Put.lang_row_en_row_code_id_with_beginning_date(
                #    old_lang_row[COLUMNS["code_id"]], self.__database, new_en_row[COLUMNS["code_id"]], self.__config.version_date)
                               # keep the term data, but inactivate the old row and create a new one
                new_lang_row = old_lang_row.copy()
                new_lang_row[COLUMNS["code_id"]] = Get.next_codeid(self.__database)
                new_lang_row = Set.lang_row_concept_columns(
                    new_lang_row, new_en_row)
                new_lang_row = Set.lang_administrative(
                    new_en_row, new_lang_row, ADMINISTRATIVE_COLUMNS)
                new_lang_row = Set.date(new_lang_row, self.__config)
                # inactivate the old lang row
                self.__database = Put.inactivate_row(old_lang_row[COLUMNS["code_id"]], self.__database, self.__config.version_date,
                                                     old_en_row[COLUMNS["inaktivoinnin_selite"]], old_en_row[COLUMNS["edit_comment"]], new_lang_row[COLUMNS["code_id"]])
                # add the new lang row to the database
                self.__database = Post.new_row_to_database_table(
                    new_lang_row, self.__database)

    def commit(self) -> 'pd.DataFrame':
        """Main function
        """

        for old_en_row, new_en_row in self.__new_term_en_rows:
            new_en_row = self.__set_en_row(new_en_row, old_en_row)
            self.__set_lang_rows(new_en_row, old_en_row)
        return self.__database
