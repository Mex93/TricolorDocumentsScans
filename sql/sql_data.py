# Название всех таблиц скрипта
class SQL_TABLE_NAME:
    tb_tricolor_keys_base = "tricolor_key_base"
    tb_tricolor_history = "tricolor_attached_history"
    tb_process_atached = "tricolor_keys_attached"
    tb_tv_models = "tv"
    tb_assembled_tv = "assembled_tv"


# Название полей в конфиге готовых тв
class SQL_KEY_BASE_SN:  # таблица созданных паллетов
    fd_assy_id = "assy_id"
    fd_tricolor_key = "tricolor_id"  #
    fd_tv_fk = "tv_fk"  #
    fd_load_key_date = "load_key_date"  #

class SQL_KEY_HISTORY:  # таблица созданных
    fd_assy_id = "assy_id"
    fd_tricolor_key = "tricolor_id"  #
    fd_load_key_date = "load_key_date"  #
    fd_attach_on_device_date = "attach_on_device_date"  #
    fd_assembled_line = "assembled_line"  #
    fd_attached_tv_sn = "used_device_sn"  #
    fd_attach_on_device_fk = "tv_fk"  #

class SQL_KEY_PROCESS_BASE:  # таблица созданных
    fd_assy_id = "assy_id"
    fd_tricolor_key = "tricolor_id"  #
    fd_tv_fk = "tv_fk"  #
    fd_used_device_sn = "used_device_sn"  #
    fd_load_key_date = "load_key_date"  #
    fd_attach_on_device_date = "attach_on_device_date"  #
    fd_assembled_line = "assembled_line"  #

class SQL_TABLE_ASSEMBLED_TV:  # Таблица собранных телевизоров
    fd_assy_id = "assy_id"
    fd_tv_fk = "tv_fk"
    fd_tv_sn = "tv_sn"  # Линия вторичный ключ

    fd_line_fk = "line_fk"
    fd_first_scan_time = "timestamp_st10"  # Время сканировки первичной
    fd_completed_scan_time = "timestamp_st100"  # Дата прохождения черезе упаковку
    fd_sn_scan_time = "timestamp_st60"  # Дата прохождения черезе присвоение sn
    fd_tricolor_key = "tricolor_id"

class SQL_TV_MODELS_DATA:  # таблица созданных
    fd_tv_id = "tv_id"
    fd_is_tricolor_id = "is_tricolor_id"  #
    fd_tv_serial_number_template = "tv_serial_number_template"  #
    fd_tv_name = "tv_name"  #

