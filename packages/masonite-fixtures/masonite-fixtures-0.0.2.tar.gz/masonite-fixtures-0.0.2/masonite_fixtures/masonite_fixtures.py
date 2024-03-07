import csv
import inspect
import logging
import os
from pathlib import Path
from typing import Any

import inflection
from masoniteorm.config import load_config
from masoniteorm.migrations import Migration
from masoniteorm.query import QueryBuilder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class FixtureMixin:
    @classmethod
    def boot_FixtureMixin(self, builder: QueryBuilder):
        pluralized_lowercase_name = inflection.pluralize(builder.get_table_name()).lower()
        self.__connection__, self.__table__, self.__resource__ = pluralized_lowercase_name, pluralized_lowercase_name, pluralized_lowercase_name
        logger.info(f"Initializing [{self.__resource__}] Fixture")
        fixture_model = builder._model
        DB = load_config().DB
        DATABASES = DB.get_connection_details()

        cache_path = Path(inspect.getfile(fixture_model.__class__)).parent / "fixture-cache"
        cache_path.mkdir(exist_ok=True)
        cache_file = cache_path / f"{self.__resource__}.sqlite3"
        self.cache_file_dir = cache_path / cache_file

        self.connection(self, pluralized_lowercase_name, fixture_model, cache_file, databases=DATABASES, db=DB)
        self.builder = QueryBuilder().on(f'{self.__resource__}').table(f'{self.__resource__}')
        return self.builder

    @staticmethod
    def connection(self, table: str, fixture_model, cache_file, databases, db) -> Any:
        logger.info(f"Connecting to [{table}] Fixture")
        # Load connection resolver and get current dictionary containing connections

        if not cache_file.exists():
            cache_file.touch()

        # Add fixture to database connection dictionary and set the updated connection details on the connection resolver
        databases.update({
            f'{table}': {
                "driver": "sqlite",
                "database": cache_file,
                "log_queries": getattr(fixture_model, "__log_queries__", False),
            }
        })
        db.set_connection_details(databases)


        self.create_table(self, fixture_model)
        self.check_data_freshness(self, fixture_model)
        return self

    def create_table(self, fixture_model):
        logger.info(f"Creating [{self.__resource__}] Fixture Table")
        table_name: str = self.__resource__

        create_table: Migration = Migration(connection=table_name)

        if getattr(fixture_model, "rows", None):
            first_row: dict[str, Any] = fixture_model.rows[0]

        if getattr(fixture_model, "get_rows", None):
            first_row: dict[str, Any] = fixture_model.get_rows()[0]


        if not getattr(fixture_model, 'rows', None) and not getattr(fixture_model, 'get_rows', None):
            raise AttributeError(
                f"[rows] attribute or [get_rows] method must be defined on the fixture model [{fixture_model.__class__.__name__}]")

        try:
            with create_table.schema.create(table_name) as table:
                table.increments("id")
                for key, value in first_row.items():
                    if key == "id":
                        continue
                    if isinstance(value, int):
                        table.integer(key).nullable()
                    elif isinstance(value, str):
                        table.string(key).nullable()
                    elif isinstance(value, float):
                        table.float(key).nullable()
                    elif isinstance(value, bool):
                        table.boolean(key).nullable()
                    else:
                        table.string(key).nullable()
                table.timestamps()
        except Exception as e:
            return None

    def migrate(self, fixture_model):
        logger.info(f"Migrating [{self.__resource__}] Fixture Data")
        if getattr(fixture_model, "get_rows", None):
            QueryBuilder().on(f'{self.__resource__}').table(f'{self.__resource__}').bulk_create(
                fixture_model.get_rows()
            )
            return fixture_model

        if getattr(fixture_model, "rows", None):
            QueryBuilder().on(f'{self.__resource__}').table(f'{self.__resource__}').bulk_create(
                fixture_model.rows
            )
            return fixture_model

        raise AttributeError(
            f"[rows] attribute or [get_rows] method must be defined on the fixture model [{self.__class__.__name__}]")

    def check_data_freshness(self, fixture_model):
        logger.info(f"Checking [{self.__resource__}] Fixture Data Freshness")
        cache_path = Path(inspect.getfile(fixture_model.__class__)).parent / "fixture-cache"
        cache_file = cache_path / f"{self.__resource__}.sqlite3"

        # Check if cache file exists
        if not cache_file.exists():
            logger.info(f"Cache file does not exist for [{self.__resource__}]")
            return self

        # Get cache file modification time
        cache_file_last_updated = cache_file.stat().st_mtime

        # Get model file modification time
        model_file_last_updated = os.path.getmtime(inspect.getfile(fixture_model.__class__))

        # If the cache file is older than the model file, refresh the data
        if cache_file_last_updated < model_file_last_updated:
            logger.info(f"Cache file is older than model file. Refreshing data for [{self.__resource__}]")
            QueryBuilder().on(f'{self.__resource__}').table(f'{self.__resource__}').delete()
            self.migrate(self, fixture_model)

        return self

    def csv_to_list_dicts(self, csv_path: str):
        myFile = open(csv_path, "r")
        reader = csv.DictReader(myFile)
        myList = list()
        for dictionary in reader:
            myList.append(dictionary)
        return myList

    def get_schema(self):
        return self.schema
