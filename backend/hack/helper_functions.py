import logging
import os
from functools import cache
from os.path import dirname

from dateutil.parser import ParserError, parse
from pymongo import MongoClient
from pymongo.collection import Collection

from hack.constants import COLLECTION_CASE, COLLECTION_CASE_REVISION


def current_file_cwd(file: str) -> str:
    return dirname(os.path.abspath(file))


@cache
def get_mongo_client():
    return MongoClient("mongodb://root:hackzurich2023pizza@localhost:27017/", uuidRepresentation="standard")


def get_mongo_collection(collection: str) -> Collection:
    mongo_client = get_mongo_client()
    db = mongo_client["hackzurich2023"]
    return db[collection]


def get_case_revision_collection() -> Collection:
    return get_mongo_collection(collection=COLLECTION_CASE_REVISION)


def get_case_collection() -> Collection:
    return get_mongo_collection(collection=COLLECTION_CASE)


def parse_date(raw_start_date: str | None):
    if not raw_start_date or "%" in raw_start_date:
        return None
    try:
        return parse(raw_start_date)
    except ParserError:
        logging.error(f'Value "{raw_start_date}" could not be parsed to a date')
        return raw_start_date
