"""
The seeding Provider is responsible for seeding the database with
initial data or random, fake data for testing purposes. This is
not recommended for production use, and should only be used for
development purposes. The seeding Provider will not overwrite
existing data, and will only seed data that does not exist.

You may enable the seeder by changing the 'SEED' variable in the
`app.py` file in the `config` directory to `True`. This will
enable the seeder to run upon start-up of the bot. If you do not
want to seed the database, you can set this to `False`. Additionally,
you can run the seeder manually by using the `seed` command.

The seeding Provider requires that the seeding files follow the
conventions dictated by the Provider, thus expecting at least
a Seeder class with a table property as well as a dictionary of
columns. Each column should be a dictionary with a name and a
value key, where the value is the seed value for the column. The
name is the column name to be seeded.

Optionally, you can choose to use the "Faker" library to generate
fake data, but we have opted not to do this by default, as it
requires an additional dependency to be installed, and we do not
want to force this dependency on the user. And was decided not
to be necessary for the purpose of this bot and the type of data
we are seeding.

class Seeder:
    table = "example"
    columns = [
        {"column_name": "column_value"},
        {"another_column_name": "column_value"},
    ]

    def getTable(self):
        return self.table

    def getColumns(self):
        return self.columns
"""
import importlib
import os

from config.directories import Directories
from utilities.database import mysql_login


async def run_seeders():
    """
    Collects all the seeder files and dynamically loads the classes, retrieving the desired seeder data
    It then inserts this data into the table if it does not already exist.
    """
    seeder_directory = Directories().get_directory("seeders")
    seeder_files = os.listdir(seeder_directory)
    cursor = await mysql_login()
    database = cursor.cursor()

    for file in seeder_files:
        if not file.endswith(".py"):
            continue

        seeder_table = file.split(".")[0]
        seeder_path = os.path.join(seeder_directory, file)

        spec = importlib.util.spec_from_file_location(seeder_table, seeder_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "Seeder"):
            raise AttributeError(f"Seeder class not found in {seeder_table}")

        Seeder = module.Seeder

        seeder_name = Seeder.getTable(self=Seeder)
        seeder_columns = Seeder.getColumns(self=Seeder)

        print(f'Running seeder {seeder_name}...')

        sanitized_query = queryBuilder(seeder_name, seeder_columns)
        seeder(sanitized_query, database, cursor)

        print(f'Finished running seeder {seeder_name}.')

    database.close()
    cursor.close()


def queryBuilder(table_name, columns_list):
    """
    Builds a query string for inserting data into a table
    :param table_name: The name of the table
    :param columns_list: List of dictionaries representing columns and their values
    :return: The query string and the corresponding values as a tuple
    """
    keys_list = [key for row in columns_list for key in row.keys()]
    keys_string = ", ".join(keys_list)
    values_list = [str(value) for row in columns_list for value in row.values()]

    placeholders = ", ".join(["%s"] * len(values_list))
    query_string = f"INSERT IGNORE INTO {table_name} ({keys_string}) VALUES ({placeholders})"

    return query_string, tuple(values_list)


def seeder(sanitized_query, database, cursor):
    """
    Runs the query strings to insert into the tables according to the seeders
    :param cursor: The database cursor
    :param sanitized_query: A tuple containing the query string and its corresponding values
    :param database: The database connection
    """
    print(sanitized_query[0], sanitized_query[1])
    database.execute(sanitized_query[0], sanitized_query[1])
    cursor.commit()
