import time
import urllib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Tuple
from lib.misc import get_conncection_dict


PYODBC_STRING = (
    "DRIVER={driver};"
    "SERVER={server};"
    "DATABASE={database};"
    "UID={userid};"
    "PWD={pwd};"
)


def create_engine_from_connection_name(
    connection_name: str,
    pool=True
):
    """
    :connection_name: Connection name, it must match with the upper
                      case of environment variables, for example: RMS
    """
    conn_params = get_conncection_dict(connection_name)
    odbc_string = PYODBC_STRING.format(
        driver=conn_params.get("driver"),
        server=conn_params.get("server"),
        database=conn_params.get("database"),
        userid=conn_params.get("uid"),
        pwd=conn_params.get("pwd"),
    )
    quoted_conn_str = urllib.parse.quote_plus(odbc_string)
    if pool:
        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={quoted_conn_str}",
            pool_size=50,
            max_overflow=5,
            connect_args={"check_same_thread": False},
        )
    else:
        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={quoted_conn_str}", pool=None
        )
    return engine
    


def create_db_connection(
    connection_name: str,
    pool=True
) -> Tuple[Session, float]:
    engine = create_engine_from_connection_name(connection_name, pool)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session()
