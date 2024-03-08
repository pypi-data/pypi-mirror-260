from typing import Any

from logger_local.MetaLogger import MetaLogger

from .constants import LOGGER_CONNECTOR_CODE_OBJECT


class Cursor(metaclass=MetaLogger, object=LOGGER_CONNECTOR_CODE_OBJECT):
    def __init__(self, cursor) -> None:
        self.cursor = cursor

    # TODO: If environment <> prod1 and dvlp1 break down using 3rd party package and analyze the formatted_sql
    #  and call private method _validate_select_table_name(table_name)
    def execute(self, sql_statement: str, sql_parameters: tuple = None) -> None:
        # TODO: validate_select_table_name(table_name)
        # TODO: remove the old approach, including the try-except
        self.logger.start("Old approach", object={
            "sql_statement": sql_statement, "sql_parameters": sql_parameters})
        try:
            if sql_parameters:
                quoted_parameters = ["'" + str(param) + "'" for param in sql_parameters]
                formatted_sql = sql_statement % tuple(quoted_parameters)
                sql_parameters_str = ", ".join(quoted_parameters)
            else:
                formatted_sql = sql_statement
                sql_parameters_str = "None"
            self.logger.info('database-mysql-local cursor.py execute()', object={
                "full_sql_query": formatted_sql,
                "sql_parameters": sql_parameters_str,
                "sql_statement": sql_statement
            })
            self.cursor.execute(sql_statement, sql_parameters)
        except Exception as exception:
            self.logger.exception("Old approach", object={
                "exception": exception,
                "sql_statement": sql_statement,
                "approach": "Old approach"
            })
            raise exception
        finally:  # called even if an exception is raised
            self.logger.end("Old approach")

    def fetchall(self) -> Any:
        return self.cursor.fetchall()

    def fetchone(self) -> Any:
        return self.cursor.fetchone()

    def description(self) -> Any:
        return self.cursor.description

    def lastrowid(self) -> int:
        return self.cursor.lastrowid

    def close(self) -> None:
        self.cursor.close()
