"""
This provider handles running the migration scripts for the database
by retrieving all the migration scripts and running them in order.

The migration Provider only handles the migration of non-existent
tables, and will not overwrite already existing tables. If you
want to regenerate all tables, you will need to manually delete
the tables or use the migration commands provided by the bot.

the migration Provider requires that the migration files follow
the conventions dictated by the Provider, thus expecting at least
a Schema class with a getName and getColumns method, as well as
the name itself, and a list of columns to be added to the table:

class Schema:
    name = "example"
    columns = [
        "column_name VARCHAR(20) PRIMARY KEY",
        "another_column INT DEFAULT 0"
    ]

    def getName(self):
        return self.name

    def getColumns(self):
        return self.columns
"""

import importlib
import os

from config.directories import Directories
from utilities.database import mysql_login

migration_directory = Directories().get_directory("migrations")
migration_files = os.listdir(migration_directory)


async def run_migrations():
    """
    Collects all the migration files and dynamically loads the classes, retrieving the desired schema data
    """

    cursor = await mysql_login()
    database = cursor.cursor()

    for file in migration_files:
        if not file.endswith(".py"):
            continue

        migration_name = file.split(".")[0]
        migration_path = os.path.join(migration_directory, file)

        spec = importlib.util.spec_from_file_location(migration_name, migration_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "Schema"):
            raise AttributeError(f"Schema class not found in {migration_name}")

        Schema = module.Schema

        schema_name = Schema.getName(self=Schema)
        schema_columns = Schema.getColumns(self=Schema)

        print(f'Running migration {schema_name}...')

        query_string = queryBuilder(schema_name, schema_columns)
        migration_handler(query_string, database)

        print(f'Finished running migration {schema_name}.')

    database.close()
    cursor.close()


def queryBuilder(table_name, columns):
    """
    Builds a query string for creating a table
    :param table_name: The name of the table
    :param columns: The columns to be added to the table
    :return: The query string
    """
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for column in columns:
        query += f"{column}, "
    query = query[:-2]
    query += ")"
    return query


def migration_handler(query_string, database):
    """
    Runs the query strings to create the tables according to the migration schemas
    :param query_string:
    :param database:
    """
    database.execute(query_string)


async def kill_active_migrations():
    """
    Kills all active migrations
    """
    cursor = await mysql_login()
    database = cursor.cursor()

    for file in migration_files:
        if not file.endswith(".py"):
            continue

        migration_name = file.split(".")[0]
        migration_path = os.path.join(migration_directory, file)

        spec = importlib.util.spec_from_file_location(migration_name, migration_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "Schema"):
            raise AttributeError(f"Schema class not found in {migration_name}")

        Schema = module.Schema

        schema_name = Schema.getName(self=Schema)

        print(f'Killing migration {schema_name}...')

        database.execute(f"DROP TABLE IF EXISTS {schema_name}")

        print(f'Killed migration {schema_name}.')
