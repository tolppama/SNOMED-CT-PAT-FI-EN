import re
import pandas as pd


class Get:
    @staticmethod
    def edit_rows(table: 'pd.DataFrame'):
        table = table[table['status'] != 'new']
        return table[(table['lineid'].duplicated(keep=False))].copy()

    @staticmethod
    def new_rows(table: 'pd.DataFrame'):
        return table[table['status'] == 'new'].copy()

    @staticmethod
    def activated_rows(table: 'pd.DataFrame'):
        return table[table['status'] == 'activated'].copy()

    @staticmethod
    def inactivated_rows(table: 'pd.DataFrame'):
        return table[table['status'] == 'inactivate'].copy()

    @staticmethod
    def en_row(table: 'pd.DataFrame'):
        return table[table['lang'] == 'en'].copy()

    @staticmethod
    def lang_rows(table: 'pd.DataFrame'):
        return table[table['lang'] != 'en'].copy()

    @staticmethod
    def lang_rows_by_en(table: 'pd.DataFrame', en_row: 'pd.DataFrame'):
        return table[table['sct_termid_en'] == en_row['sct_termid_en']].copy()

    @staticmethod
    def old_row(table: 'pd.DataFrame'):
        return table[table['status'] != 'edit'].iloc[0]

    @staticmethod
    def new_row(table: 'pd.DataFrame'):
        return table[table['status'] == 'edit'].iloc[0]

    @staticmethod
    def table_index(table: 'pd.DataFrame', row: 'pd.DataFrame'):
        return table.loc[table['lineid'] ==
                         row['lineid']].index[0]

    @staticmethod
    def index_by_codeid(table: 'pd.DataFrame', lineid: int):
        return table.loc[table['lineid'] == int(lineid)].index.values[0]

    @staticmethod
    def row_by_codeid(table: 'pd.DataFrame', lineid: int):
        return table[table['lineid'] == lineid].copy()

    @staticmethod
    def row_by_index(table: 'pd.DataFrame', index: int):
        return table.iloc[index].copy()

    @staticmethod
    def get_next_codeid(table: 'pd.DataFrame'):
        return int(table['lineid'].astype(int).max() + 1)

    @staticmethod
    def get_legacyid(self, row: 'pd.DataFrame', column: str):
        legacyid = row[column]
        if not re.fullmatch(r".+-\d*", legacyid):
            return None
        sn2, sct_id = legacyid.split('-')
        return sn2 or None, sct_id or None
    
    @staticmethod
    def next_fin_extension_id(table: 'pd.DataFrame', column: str) -> int:
        fin_id_series = table[column][table[column].str.fullmatch(
            r"^\d+1000288(10|11)\d$") == True]
        fin_id_max = 0

        if not fin_id_series.empty:
            fin_id_series = fin_id_series.apply(lambda x: x[:len(x)-10])
            fin_id_series = fin_id_series.astype(int)
            fin_id_max = fin_id_series.max()
        fin_id_max += 1
        return fin_id_max
