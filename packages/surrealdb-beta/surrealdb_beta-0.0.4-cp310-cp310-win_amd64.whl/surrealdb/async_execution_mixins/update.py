"""
This file defines the interface between python and the Rust SurrealDB library for updating rows in the database. 
"""
import json
from typing import List, Union

from surrealdb.rust_surrealdb import rust_merge_future
from surrealdb.rust_surrealdb import rust_update_future
from surrealdb.rust_surrealdb import rust_patch_future

from surrealdb.errors import SurrealDbError


class AsyncUpdateMixin:
    """
    This class is responsible for the interface between python and the Rust SurrealDB library for creating a document.
    """
    async def update(self: "SurrealDB", resource: str, data: dict) -> Union[List[dict], dict]:
        """
        Updates the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to update the resource with
        :return: the updated resource such as an individual row or a list of rows
        """
        try:
            return json.loads(await rust_update_future(self._connection, resource, json.dumps(data)))
        except Exception as e:
            raise SurrealDbError(e)

    async def merge(self: "SurrealDB", resource: str, data: dict) -> Union[List[dict], dict]:
        """
        Merges the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to merge the resource with
        :return: the updated resource such as an individual row or a list of rows
        """
        try:
            return json.loads(await rust_merge_future(self._connection, resource, json.dumps(data)))
        except Exception as e:
            raise SurrealDbError(e)

    async def patch(self: "SurrealDB", resource: str, data: dict) -> Union[List[dict], dict]:
        """
        Patches the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to patch the resource with
        :return: the updated resource such as an individual row or a list of rows
        """
        try:
            return json.loads(await rust_patch_future(self._connection, resource, json.dumps(data)))
        except Exception as e:
            raise SurrealDbError(e)
