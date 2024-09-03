from sql.CSQLAgent import CSqlAgent
from sql.sql_data import (SQL_TABLE_NAME,
                          SQL_KEY_HISTORY,
                          SQL_KEY_PROCESS_BASE,
                          SQL_KEY_BASE_SN,
                          SQL_TABLE_ASSEMBLED_TV,
                          SQL_TV_MODELS_DATA)

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

    def get_assembled_tv_from_tricolor_key(self, tricolor_key: str) -> tuple | bool:
        query_string = (f"SELECT "
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key},"
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tv_fk},"
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tv_sn} "
                        f"FROM {SQL_TABLE_NAME.tb_assembled_tv} "
                        f"WHERE {SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tricolor_key,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_sn = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_sn, None)
        tricolor_key = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key, None)
        tv_fk = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_fk, None)
        ret_tup = (tv_sn, tv_fk, tricolor_key)
        return ret_tup

    def get_assembled_tv_from_tv_sn(self, tv_sn: str) -> tuple | bool:
        query_string = (f"SELECT "
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key},"
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tv_fk},"
                        f"{SQL_TABLE_ASSEMBLED_TV.fd_tv_sn} "
                        f"FROM {SQL_TABLE_NAME.tb_assembled_tv} "
                        f"WHERE {SQL_TABLE_ASSEMBLED_TV.fd_tv_sn} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tv_sn,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_sn = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_sn, None)
        tv_fk = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_fk, None)
        tricolor_key = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key, None)
        ret_tup = (tv_sn, tv_fk, tricolor_key)
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
        load_date = str(result[0].get(SQL_KEY_BASE_SN.fd_load_key_date, None))

        ret_tup = (tv_fk, load_date)
        return ret_tup

    def get_tricolor_key_data_in_history_base(self, tricolor_key: str) -> tuple | bool:
        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.tb_tricolor_history} "
                        f"WHERE {SQL_KEY_HISTORY.fd_tricolor_key} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tricolor_key,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        assembled_line = result[0].get(SQL_KEY_HISTORY.fd_assembled_line, None)
        tv_sn = result[0].get(SQL_KEY_HISTORY.fd_attached_tv_sn, None)
        attached_date = result[0].get(SQL_KEY_HISTORY.fd_attach_on_device_date, None)
        create_date = result[0].get(SQL_KEY_HISTORY.fd_load_key_date, None)
        tv_fk = result[0].get(SQL_KEY_HISTORY.fd_attach_on_device_fk, None)

        ret_tup = (tv_sn, tv_fk, assembled_line, attached_date, create_date)
        return ret_tup

    def get_tricolor_key_data_in_process_base(self, tricolor_key: str) -> tuple | bool:
        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.process_atached} "
                        f"WHERE {SQL_KEY_PROCESS_BASE.fd_tricolor_key} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tricolor_key,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        assembled_line = result[0].get(SQL_KEY_PROCESS_BASE.fd_assembled_line, None)
        tv_sn = result[0].get(SQL_KEY_PROCESS_BASE.fd_used_device_sn, None)
        attached_date = result[0].get(SQL_KEY_PROCESS_BASE.fd_attach_on_device_date, None)
        create_date = result[0].get(SQL_KEY_PROCESS_BASE.fd_load_key_date, None)
        tv_fk = result[0].get(SQL_KEY_PROCESS_BASE.fd_tv_fk, None)

        ret_tup = (tv_sn, tv_fk, assembled_line, attached_date, create_date)
        return ret_tup


    # def is_created_pallet(self, pallet_code: str):
    #     """А создан ли вообще паллет"""
    #     query_string = (f"SELECT {SQL_PALLET_SN.fd_assy_id} "
    #                     f"FROM {SQL_TABLE_NAME.tb_pallet_sn} "
    #                     f"WHERE {SQL_PALLET_SN.fd_pallet_code} = %s "
    #                     f"LIMIT 1")  # на всякий лимит
    #
    #     result = self.sql_query_and_get_result(
    #         self.get_sql_handle(), query_string, (pallet_code,), "_1", )  # Запрос типа аасоциативного массива
    #     if result is False:  # Errorrrrrrrrrrrrr based data
    #         return False
    #
    #     sql_pass = result[0].get(SQL_PALLET_SN.fd_assy_id, None)
    #     if sql_pass is not None:
    #         return True
    #
    #     return False
    #
    # def is_created_pallet_completed(self, pallet_code: str):
    #     """А скомпликтован ли паллет вообще"""
    #     query_string = (
    #         f"SELECT {SQL_TABLE_NAME.tb_pallet_sn}.{SQL_PALLET_SN.fd_completed_check}, COUNT(*) as tv_counts "
    #         f"FROM {SQL_TABLE_NAME.tb_pallet_sn} "
    #         f"JOIN {SQL_TABLE_NAME.tb_pallet_scanned} "
    #         f"ON {SQL_TABLE_NAME.tb_pallet_sn}.{SQL_PALLET_SN.fd_pallet_code} = "
    #         f"{SQL_TABLE_NAME.tb_pallet_scanned}.{SQL_PALLET_SCANNED.fd_fk_pallet_code} "
    #         f"WHERE {SQL_TABLE_NAME.tb_pallet_sn}.{SQL_PALLET_SN.fd_pallet_code} = %s "
    #         f"GROUP BY 1"
    #         )  # на всякий лимит
    #
    #     result = self.sql_query_and_get_result(
    #         self.get_sql_handle(), query_string, (pallet_code,), "_1", )  # Запрос типа аасоциативного массива
    #     if result is False:  # Errorrrrrrrrrrrrr based data
    #         return False
    #
    #     sql_pass = result[0].get(SQL_PALLET_SN.fd_completed_check, None)
    #     if sql_pass is None:
    #         return False
    #
    #     if sql_pass is False:  # комплектность чек
    #         return False
    #
    #     count = result[0].get("tv_counts", None)
    #     if count == 0 or count is None:
    #         return False
    #
    #     return count
    #
    # def get_device_sn_in_pallet(self, pallet_code: str):
    #     """Инфа о паллете"""
    #     query_string = (f"SELECT {SQL_PALLET_SCANNED.fd_tv_sn} "
    #                     f"FROM {SQL_TABLE_NAME.tb_pallet_scanned} "
    #                     f"WHERE {SQL_PALLET_SCANNED.fd_fk_pallet_code} = %s "
    #                     f"LIMIT 100")  # на всякий лимит
    #
    #     result = self.sql_query_and_get_result(
    #         self.get_sql_handle(), query_string, (pallet_code,), "_1", )  # Запрос типа аасоциативного массива
    #     if result is False:  # Errorrrrrrrrrrrrr based data
    #         return False
    #     # print(result)
    #     if len(result) > 0:
    #         return result
    #
    #     return None
