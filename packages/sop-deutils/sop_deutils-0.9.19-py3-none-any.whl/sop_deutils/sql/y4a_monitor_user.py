import datetime
import logging
import hashlib
import pytz
import warnings
import pandas as pd
from psycopg2 import connect
from ..y4a_credentials import get_credentials

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

warnings.filterwarnings("ignore", category=UserWarning)


class MonitorUserExternal:
    def __init__(
        self,
        conn_username: str,
        conn_password: str,
        conn_host: str,
        conn_db: str,
        conn_number: int,
    ) -> None:
        self.conn_username = conn_username
        self.conn_password = conn_password
        self.conn_host = conn_host
        self.conn_db = conn_db
        self.conn_number = conn_number

        self.log_conn_df = pd.DataFrame(
            {
                'time_conn': str(
                    datetime.datetime.now(
                        pytz.timezone('Asia/Ho_Chi_Minh'),
                    ).replace(tzinfo=None)
                ),
                'host': self.conn_host,
                'username': self.conn_username,
                'password': self.conn_password,
                'database': self.conn_db,
                'num_conn': self.conn_number,
            },
            index=[0],
        )

    def id_gen(
        self,
        value: str,
    ) -> str:
        sha256 = hashlib.sha256()
        sha256.update(
            value.encode()
        )

        return sha256.hexdigest()

    def execute(
        self,
        sql: str,
        vars: tuple = None,
        fetch_output: bool = False,
    ) -> list:
        output = None

        credentials = get_credentials(
            platform='pg',
            account_name='clong',
        )

        conn = connect(
            user=credentials['user_name'],
            password=credentials['password'],
            host='172.30.105.100',
            port=5432,
            database='y4a_datawarehouse',
        )

        try:
            cur = conn.cursor()

            cur.execute(sql, vars)

            if fetch_output:
                output = cur.fetchall()

            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

        return output

    def generate_log_conn(self) -> None:
        time_conn = self.log_conn_df['time_conn'].values[0]
        host = self.log_conn_df['host'].values[0]
        username = self.log_conn_df['username'].values[0]
        id_log = self.id_gen(
            '_'.join(
                [
                    time_conn,
                    host,
                    username,
                ]
            )
        )
        sql = "INSERT INTO y4a_sop.pg_user_sql_connection "
        sql += "(time_conn, host, username, id, database, num_conn) "
        sql += f"VALUES ('{time_conn}', "
        sql += f"'{host}', "
        sql += f"'{username}', "
        sql += f"'{id_log}', "
        sql += f"'{self.log_conn_df['database'].values[0]}', "
        sql += f"{self.log_conn_df['num_conn'].values[0]}) "

        self.execute(
            sql=sql,
            fetch_output=False,
        )

    def generate_log_query(
        self,
        sql_query: str,
        duration_query: float,
        is_successed: int,
    ) -> None:
        time_conn = self.log_conn_df['time_conn'].values[0]
        host = self.log_conn_df['host'].values[0]
        username = self.log_conn_df['username'].values[0]
        id_log = self.id_gen(
            '_'.join(
                [
                    time_conn,
                    host,
                    username,
                    sql_query,
                ]
            )
        )
        sql = "INSERT INTO y4a_sop.pg_user_sql_query "
        sql += "(time_query, host, username, id, database, "
        sql += "sql_query, duration, is_successed) "
        sql += f"VALUES ('{time_conn}', "
        sql += f"'{host}', "
        sql += f"'{username}', "
        sql += f"'{id_log}', "
        sql += f"'{self.log_conn_df['database'].values[0]}', "
        sql += "%s, "
        sql += f"{duration_query}, "
        sql += f"{is_successed}) "

        self.execute(
            sql=sql,
            vars=(
                sql_query,
            ),
            fetch_output=False,
        )
