import boto3
from botocore.config import Config
import pandas as pd
from pyqldb.driver.qldb_driver import QldbDriver
import logging


def convert_to_df(query_return):
    """
    Convert the query return value to a pandas DataFrame.

    :param query_return: The return value from a query execution.
    :return: A pandas DataFrame constructed from the query return value.
    """
    return pd.DataFrame(query_return)


def convert_to_dicts(query_return):
    """
    Convert the query return value to a list of dictionaries, where each dictionary represents a row from the result.

    :param query_return: The return value from a query execution.
    :return: A list of dictionaries, each representing a row from the query return result.
    """
    return convert_to_df(query_return).to_dict(orient="records")


class LedgerHelper:
    def __init__(self, ledger_name: str, table_name: str, index_name:str, extension: str=None, credentials: dict=None,
                 region: str=None, bypass_boto=False):
        """
        Initialize the LedgerHelper class to assist with operations on a specified QLDB ledger.

        :param ledger_name: The name of the QLDB ledger.
        :param table_name: The name of the table within the ledger.
        :param index_name: The primary index name of the table.
        :param extension: Optional. Appends to the ledger name for testing, isolating branches by creating new tables without removing them post-tests.
        :param credentials: Optional. A dictionary containing AWS credentials (AccessKeyId, SecretAccessKey, SessionToken).
        :param region: Optional. The AWS region where the ledger is located, e.g., 'eu-central-1'.
        :param bypass_boto: If True, bypasses the boto3 client setup. Useful for testing or alternative configurations.
        """

        self.index_name = index_name
        self.table_name = table_name
        if extension is not None:
            ledger_name = f'{ledger_name}-{extension}'
        else:
            logging.info("Production environment ledger active")

        if not bypass_boto:
            if credentials is not None:
                qldb_client = boto3.client("qldb",
                                           aws_access_key_id=credentials['AccessKeyId'],
                                           aws_secret_access_key=credentials['SecretAccessKey'],
                                           aws_session_token=credentials['SessionToken'],
                                           config=Config(region_name=region))
            else:
                if not region:
                    qldb_client = boto3.client("qldb")
                else:
                    qldb_client = boto3.client("qldb", config=Config(region_name=region))

            ledgers = [data['Name'] for data in qldb_client.list_ledgers(MaxResults=20)["Ledgers"]]

            if ledger_name not in ledgers:
                logging.info(f"Creating ledger with name {ledger_name}. This may take a few minutes")
                qldb_client.create_ledger(Name=ledger_name,
                                          PermissionsMode='STANDARD')

        self.ledger_driver = QldbDriver(ledger_name=ledger_name, region_name=region)

        if self.table_name not in self.ledger_driver.list_tables():
            self.initiate_table(table_name=self.table_name, index_name=self.index_name)

        logging.info(f"Ledger: {ledger_name}\nTable: {self.table_name}\nMain index: {self.index_name}\n")

    def initiate_table(self, table_name, index_name):
        """
        Create a new table and a primary index within the ledger.

        :param table_name: The name of the table to be created.
        :param index_name: The primary index name for the new table.
        """
        self.execute_query(query=f"CREATE TABLE {table_name}")
        self.execute_query(query=f"CREATE INDEX ON {table_name} ({index_name})")

    def execute_query(self, query: str, transaction_executor=None, query_arg=None):
        """
        Execute a specified query against the ledger. If a transaction executor is not provided, it creates one.

        :param query: The query string to be executed.
        :param transaction_executor: Optional. The transaction executor to use for the query.
        :param query_arg: Optional. Arguments for the query.
        :return: The result of the query execution.
        """
        if not transaction_executor:
            return self.ledger_driver.execute_lambda(lambda executor: self.execute_query(query=query,
                                                                                         transaction_executor=executor,
                                                                                         query_arg=query_arg))
        if query_arg is not None:
            return transaction_executor.execute_statement(query, query_arg)
        else:
            return transaction_executor.execute_statement(query)

    def read_entry(self, index: tuple = (None, None), column: str = None, indices: list = None):
        """
        Read entries from the table based on specified conditions.

        :param index: A tuple specifying a single index condition. Deprecated in favor of 'indices'.
        :param column: The column(s) to retrieve. '*' retrieves all columns.
        :param indices: A list of tuples specifying multiple index conditions.
        :return: The result of the query execution.
        """
        column = column or "*"

        # Initialize the WHERE clause parts list
        where_clauses = []

        # Handle the single index case for backward compatibility
        if index[0]:
            index_value = self.convert_index(index=index)
            where_clauses.append(f"{index[0]} IN ({index_value})")

        # Handle the new indices parameter
        if indices:
            # Loop through each tuple in the indices list
            for col, value in indices:
                # Check if value is a string and contains commas for multiple values
                if isinstance(value, str) and ',' in value:
                    values = [f"'{val.strip()}'" for val in value.split(',')]
                    values_str = ", ".join(values)
                else:
                    # Handle non-string or single value cases
                    if isinstance(value, str):
                        values_str = f"'{value}'"
                    else:
                        values_str = str(value)
                # Append the IN clause for this column to the where_clauses list
                where_clauses.append(f"{col} IN ({values_str})")

        # Construct the WHERE clause by joining all conditions with AND
        where_clause = " AND ".join(where_clauses)

        if where_clause:
            # Execute query with WHERE clause if there are conditions
            query = f"SELECT {column} FROM {self.table_name} WHERE {where_clause}"
        else:
            # If no conditions, execute a query to select all entries
            query = f"SELECT {column} FROM {self.table_name}"

        return self.execute_query(query=query)

    def add_entry(self, data: dict):
        """
        Insert a new entry into the table.

        :param data: A dictionary representing the data to be inserted into the table.
        """
        self.execute_query(f"INSERT INTO {self.table_name} VALUE {data}")

    def modify_entry(self, data: dict, index: tuple = (None, None)):
        """
        Update an existing entry in the table based on the specified index.

        :param data: A dictionary representing the new data for the entry.
        :param index: A tuple specifying the index of the entry to be updated.
        """
        data = data.copy()
        if not index[0]:
            index = (self.index_name, data[self.index_name])
            index_value = self.convert_index(index=index)
            del data[self.index_name]
        else:
            index_value = self.convert_index(index=index)

        for key, value in data.items():
            logging.info("updating ", key, value)
            self.execute_query(f"UPDATE {self.table_name} SET {key} = ? WHERE {index[0]} IN ({index_value})", query_arg=value)

    def remove_entry(self, data: tuple = None):
        """
         Remove an entry from the table based on the specified index.

         :param data: A tuple specifying the index of the entry to be removed.
         """
        index_value = self.convert_index(data)
        self.execute_query(f"DELETE FROM {self.table_name} WHERE {data[0]} = {index_value}")

    def add_index(self, index_name):
        """
        Create a new index on the table.

        :param index_name: The name of the new index to be created.
        """
        self.execute_query(f"CREATE INDEX ON {self.table_name}({index_name})")

    def convert_index(self, index: tuple = (None, None)):
        """
        Convert the given index tuple to a format suitable for use in queries.

        :param index: A tuple containing the index name and value.
        :return: A string representation of the index value suitable for use in a query.
        """
        if type(index[1]) == str:
            index_value = f"'{index[1]}'"
        elif type(index[1]) == list:
            index_value = str(index[1])[1:-1]
        else:
            index_value = index[1]
        return index_value


if __name__ == "__main__":
    lh = LedgerHelper(ledger_name="dgtl-pyqldb-tests", table_name="test_ledger", index_name="test_id", region="eu-west-1", bypass_boto=True)

    entries = convert_to_dicts(lh.read_entry())
    print(entries)

    for entry in entries:
        print(entry)
        lh.remove_entry(data=entry)
