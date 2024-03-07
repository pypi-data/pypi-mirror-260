import json
import sys
from typing import Iterable

import requests


# from cobweb import Seed


def struct_table_name(table_name):
    return table_name.replace(".", "__p__").replace(":", "__c__")


def restore_table_name(table_name):
    return table_name.replace("__p__", ".").replace("__c__", ":")


def struct_queue_name(db_name, table_name):
    return sys.intern(f"__{db_name}_{table_name}_queue__")


# class StorerDB:
#
#     @staticmethod
#     def console(self):
#         from db.storer.console import Console
#         table = struct_table_name(table)
#         return StorerInfo(DB=Console, table=table, length=length, config=None)
#
#     @staticmethod
#     def textfile(table, length=200):
#         from db.storer.textfile import Textfile
#         table = struct_table_name(table)
#         return StorerInfo(DB=Textfile, table=table, length=length, config=None)
#
#     @staticmethod
#     def loghub(table, length=200, config=None):
#         from db.storer.loghub import Loghub
#         table = struct_table_name(table)
#         return StorerInfo(DB=Loghub, table=table, length=length, config=config)


def parse_info(info):
    if not info:
        return info

    if isinstance(info, dict):
        return info

    if isinstance(info, str):
        return json.loads(info)

    if isinstance(info, Iterable):
        result = list()
        for ii in info:
            if isinstance(ii, str):
                result.append(json.loads(ii))
            elif isinstance(ii, dict):
                result.append(ii)
            else:
                raise TypeError("must be in [str, dict]")

        return result


def struct_start_seeds(seeds):
    from .bbb import Seed
    if not seeds:
        return None
    if any(isinstance(seeds, t) for t in (list, tuple)):
        return [Seed(seed) for seed in seeds]
    elif any(isinstance(seeds, t) for t in (str, dict)):
        return Seed(seeds)


# def get_storer_db(db):
#
#     if isinstance(db, str):
#         model = import_module(f" db.storer.{db.lower()}")
#
#         # if db.lower() in dir(StorerDB):
#         #     return getattr(StorerDB, db)
#         # else:
#         #     pass



