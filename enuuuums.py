from enum import IntEnum, auto

class SMBOX_ICON_TYPE(IntEnum):
    ICON_NONE = auto(),
    ICON_WARNING = auto(),
    ICON_ERROR = auto(),
    ICON_INFO = auto()

class INPUT_TYPE(IntEnum):
    NONE = auto(),
    TV_SN = auto(),
    TV_FK = auto(),
    TRICOLOR_ID = auto(),

