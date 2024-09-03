from sql.CSQLAgent import CSqlAgent
from sql.sql_data import (SQL_TABLE_NAME,
                          SQL_KEY_HISTORY,
                          SQL_KEY_PROCESS_BASE,
                          SQL_KEY_BASE_SN,
                          SQL_TABLE_ASSEMBLED_TV,
                          SQL_TV_MODELS_DATA)

from enuuuums import INPUT_TYPE


class CSQLQuerys(CSqlAgent):

    def __init__(self):
        super().__init__()

    def get_tv_model_data(self, tv_model_id: int) -> tuple | bool:
        query_string = (f"SELECT "
                        f"{SQL_TV_MODELS_DATA.fd_tv_name}, "
                        f"{SQL_TV_MODELS_DATA.fd_tv_serial_number_template}, "
                        f"{SQL_TV_MODELS_DATA.fd_is_tricolor_id} "
                        f"FROM {SQL_TABLE_NAME.tb_tv_models} "
                        f"WHERE {SQL_TV_MODELS_DATA.fd_tv_id} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tv_model_id,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_name = result[0].get(SQL_TV_MODELS_DATA.fd_tv_name, None)
        tv_template = result[0].get(SQL_TV_MODELS_DATA.fd_tv_serial_number_template, None)
        is_tricolor = result[0].get(SQL_TV_MODELS_DATA.fd_is_tricolor_id, None)
        if None in (tv_name, tv_template, is_tricolor):
            return False
        ret_tup = (tv_template, tv_name, is_tricolor)
        return ret_tup

    def get_assembled_tv_from_tricolor_key(self, itype: INPUT_TYPE, tv_data: str) -> tuple | bool:
        if itype == itype.TRICOLOR_ID:
            find_field = SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key
        elif itype == itype.TV_SN:
            find_field = SQL_TABLE_ASSEMBLED_TV.fd_tv_sn
        else:
            return False

        query_string = (f"SELECT "
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key},"
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tv_fk},"
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tv_sn}, "
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_completed_scan_time} "
                        f"FROM {SQL_TABLE_NAME.tb_assembled_tv} "
                        f"WHERE {find_field} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tv_data,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        date = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_completed_scan_time, None)
        tv_sn = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_sn, None)
        tricolor_key = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key, None)
        tv_fk = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_fk, None)
        ret_tup = (tv_sn, tv_fk, tricolor_key, date)
        return ret_tup

    def get_tricolor_key_data_in_key_base(self, tricolor_key: str) -> tuple | bool:
        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.tb_tricolor_keys_base} "
                        f"WHERE {SQL_KEY_BASE_SN.fd_tricolor_key} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tricolor_key,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_fk = result[0].get(SQL_KEY_BASE_SN.fd_tv_fk, None)
        load_date = result[0].get(SQL_KEY_BASE_SN.fd_load_key_date, None)

        ret_tup = (tv_fk, load_date)
        return ret_tup

    def get_tricolor_key_data_in_history_base(self, itype: INPUT_TYPE, any_data: str) -> tuple | bool:
        if itype == itype.TRICOLOR_ID:
            find_field = SQL_KEY_HISTORY.fd_tricolor_key
        elif itype == itype.TV_SN:
            find_field = SQL_KEY_HISTORY.fd_attached_tv_sn
        else:
            return False

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.tb_tricolor_history} "
                        f"WHERE {find_field} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (any_data,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tricolor_id = result[0].get(SQL_KEY_HISTORY.fd_tricolor_key, None)
        assembled_line = result[0].get(SQL_KEY_HISTORY.fd_assembled_line, None)
        tv_sn = result[0].get(SQL_KEY_HISTORY.fd_attached_tv_sn, None)
        attached_date = result[0].get(SQL_KEY_HISTORY.fd_attach_on_device_date, None)
        create_date = result[0].get(SQL_KEY_HISTORY.fd_load_key_date, None)
        tv_fk = result[0].get(SQL_KEY_HISTORY.fd_attach_on_device_fk, None)

        ret_tup = (tv_sn, tv_fk, tricolor_id, assembled_line, attached_date, create_date)
        return ret_tup

    def get_tricolor_key_data_in_process_base(self, itype: INPUT_TYPE, any_data: str) -> tuple | bool:

        if itype == itype.TRICOLOR_ID:
            find_field = SQL_KEY_PROCESS_BASE.fd_tricolor_key
        elif itype == itype.TV_SN:
            find_field = SQL_KEY_PROCESS_BASE.fd_used_device_sn
        else:
            return False

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.tb_process_atached} "
                        f"WHERE {find_field} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (any_data,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tricolor_id = result[0].get(SQL_KEY_PROCESS_BASE.fd_tricolor_key, None)
        assembled_line = result[0].get(SQL_KEY_PROCESS_BASE.fd_assembled_line, None)
        tv_sn = result[0].get(SQL_KEY_PROCESS_BASE.fd_used_device_sn, None)
        attached_date = result[0].get(SQL_KEY_PROCESS_BASE.fd_attach_on_device_date, None)
        create_date = result[0].get(SQL_KEY_PROCESS_BASE.fd_load_key_date, None)
        tv_fk = result[0].get(SQL_KEY_PROCESS_BASE.fd_tv_fk, None)

        ret_tup = (tv_sn, tv_fk, tricolor_id, assembled_line, attached_date, create_date)
        return ret_tup

    def get_tricolor_empty_key_from_key_base(self, tv_fk: int) -> tuple | bool:
        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.tb_tricolor_keys_base} "
                        f"WHERE {SQL_KEY_BASE_SN.fd_tv_fk} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tv_fk,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_fk = result[0].get(SQL_KEY_BASE_SN.fd_tv_fk, None)
        tricolor_key = result[0].get(SQL_KEY_BASE_SN.fd_tricolor_key, None)
        load_date = result[0].get(SQL_KEY_BASE_SN.fd_load_key_date, None)

        ret_tup = (tv_fk, tricolor_key, load_date)
        return ret_tup

    def insert_key_in_attached_base(self, tv_fk: int, tv_sn: str, tricolor_key: str, assembled_line: int,
                                    load_date) -> bool:

        query_string = (f"INSERT INTO {SQL_TABLE_NAME.tb_process_atached} "
                        f"({SQL_KEY_PROCESS_BASE.fd_tv_fk}, "
                        f"{SQL_KEY_PROCESS_BASE.fd_load_key_date}, "
                        f"{SQL_KEY_PROCESS_BASE.fd_assembled_line}, "
                        f"{SQL_KEY_PROCESS_BASE.fd_tricolor_key}, "
                        f"{SQL_KEY_PROCESS_BASE.fd_used_device_sn})"
                        f"VALUES (%s, %s, %s, %s, %s) RETURNING {SQL_KEY_PROCESS_BASE.fd_assy_id}")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tv_fk, load_date, assembled_line, tricolor_key, tv_sn),
            "_i", transaction=True)  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        return True

    def delete_key_from_key_base(self, tv_fk: int, tricolor_key: str) -> bool:

        query_string = (f"DELETE FROM "
                        f"{SQL_TABLE_NAME.tb_tricolor_keys_base} "
                        f"WHERE "
                        f"{SQL_KEY_BASE_SN.fd_tv_fk} = %s AND "
                        f"{SQL_KEY_BASE_SN.fd_tricolor_key} = %s")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tv_fk, tricolor_key),
            "_d", transaction=True)  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        return True
