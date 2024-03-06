import os
from typing import Iterator, Any, overload

import pandas as pd
import awswrangler as wr


def get_database() -> str | None:
    database = os.getenv("TENANT", os.getenv("WR_DATABASE", None))
    return database


def get_s3_output(workgroup=None) -> str | None:
    tenant = os.getenv("TENANT", None)
    if tenant is None:
        return None

    if workgroup is None:
        workgroup = os.getenv("WR_WORKGROUP", "primary")

    workgroup_info = wr.athena.get_work_group(workgroup=workgroup)
    try:
        output_location = workgroup_info["WorkGroup"]["Configuration"]["ResultConfiguration"]["OutputLocation"]
    except KeyError:
        return None

    if workgroup_info["WorkGroup"]["Configuration"]["EnforceWorkGroupConfiguration"]:
        raise ValueError("EnforceWorkGroupConfiguration is set to True, cannot override OutputLocation")
    return f"{output_location}/{tenant}"


@overload
def read_sql_query(
    sql: str,
    database: str | None,
    chunksize: None = None,
    **kwargs
) -> pd.DataFrame:
    ...


@overload
def read_sql_query(
    sql: str,
    database: str | None,
    chunksize: int | bool,
    **kwargs
) -> Iterator[pd.DataFrame]:
    ...


def read_sql_query(
    sql: str,
    database: str | None = None,
    chunksize: int | bool | None = None,
    **kwargs
) -> pd.DataFrame | Iterator[pd.DataFrame]:
    """s3_output is required in order to ensure we separate tenant specific outputs in different locations"""
    database = database if database is not None else get_database()
    if database is None:
        raise ValueError("Database is not set")
    s3_output = kwargs.pop(
        "s3_output",
        get_s3_output(workgroup=kwargs.get("workgroup", None))
    )
    return wr.athena.read_sql_query(sql, database, s3_output=s3_output, chunksize=chunksize, **kwargs)


def start_query_execution(
    sql: str,
    database: str | None = None,
    s3_output: str | None = None,
    workgroup: str | None = None,
    **kwargs
) -> str | dict[str, Any]:
    """s3_output is required in order to ensure we separate tenant specific outputs in different locations"""
    database = database if database is not None else get_database()
    s3_output = s3_output if s3_output is not None else get_s3_output(workgroup=workgroup)
    return wr.athena.start_query_execution(
        sql,
        database,
        s3_output=s3_output,
        workgroup=workgroup,
        **kwargs
    )


def create_ctas_table(
    sql: str,
    database: str | None = None,
    s3_output: str | None = None,
    workgroup: str | None = None,
    **kwargs,
):
    database = database if database is not None else get_database()
    s3_output = s3_output if s3_output is not None else get_s3_output(workgroup=workgroup)
    return wr.athena.create_ctas_table(
        sql,
        database,
        s3_output=s3_output,
        workgroup=workgroup,
        **kwargs
    )
