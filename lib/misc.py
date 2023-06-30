import re
from typing import List, Optional, Tuple


from core import config


def obtain_error_code_from_exception(ex: Exception):
    message = str(ex)
    search = re.search(r"\[([^)]+)\]", message)
    res = (9999, message)
    if search:
        try:
            error_code, message = re.split(r"\[|\]", message)[1:3]
            res = (int(error_code), message)
        except ValueError:
            # There's no error code in the brackets
            res = (9999, message)
        except AttributeError:
            # No brackets were found or incomplete closing
            res = (9999, message)
    return res


def get_conncection_dict(db_description: str):
    """
    - db_decription:
        db prefix, eg: rms, mssql_log
    """
    db_description = db_description.upper()
    settings = config.Settings().dict()
    return {
        "driver": settings.get(f"{db_description}_DRIVER"),
        "server": settings.get(f"{db_description}_SERVER"),
        "database": settings.get(f"{db_description}_DATABASE"),
        "uid": settings.get(f"{db_description}_UID"),
        "pwd": settings.get(f"{db_description}_PWD"),
        "port": settings.get(f"{db_description}_PORT", 1443),
    }

