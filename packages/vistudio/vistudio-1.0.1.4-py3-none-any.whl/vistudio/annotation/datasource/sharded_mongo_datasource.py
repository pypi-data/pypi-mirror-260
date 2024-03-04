# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
"""
ShardedMongoDatasource
"""

import logging
from typing import Dict, List, Optional, Callable
import bson
import pymongo
import pymongoarrow.api

from ray.util.annotations import PublicAPI
from ray.data.block import Block, BlockMetadata
from ray.data.datasource.datasource import ReadTask
from ray.data.datasource.mongo_datasource import MongoDatasource


logger = logging.getLogger(__name__)


@PublicAPI(stability="alpha")
class ShardedMongoDatasource(MongoDatasource):
    """Datasource for reading from and writing to MongoDB."""
    def __init__(
        self,
        uri: str,
        database: str,
        collection: str,
        pipeline: Optional[List[Dict]] = None,
        pipeline_func: Optional[Callable[[], Block]] = None,
        schema: Optional["pymongoarrow.api.Schema"] = None,
        **mongo_args,
    ):
        """
        Args:
        uri: The URI of the MongoDB cluster.
        database: The database to read from.
        collection: The collection to read from.
        pipeline: The aggregation pipeline to apply.
        pipeline_func: A function that takes a pymongo.MongoClient and returns a Block.
        schema: The schema to use for reading.
        mongo_args: Additional arguments to pass to the pymongo.MongoClient constructor.
        """
        self._pipeline_func = pipeline_func
        super().__init__(uri, database, collection, pipeline=pipeline, schema=schema, **mongo_args)



    def get_read_tasks(self, parallelism: int) -> List[ReadTask]:
        def make_block(
            uri: str,
            database: str,
            collection: str,
            pipeline: List[Dict],
            pipeline_func: Optional[Callable[[], Block]],
            shard_match: Dict,
            shard_hosts: List[str],
            schema: "pymongoarrow.api.Schema",
            kwargs: dict,
        ) -> Block:
            import pymongo
            from pymongo.uri_parser import parse_uri
            from pymongoarrow.api import aggregate_arrow_all

            # A range query over the partition.
            match = [
                {
                    "$match": shard_match,
                }
            ]

            uri_info = parse_uri(uri)
            uri_info["nodelist"] = shard_hosts
            shard_uri = _to_mongo_uri(uri_info)
            client = pymongo.MongoClient(shard_uri)

            if pipeline_func is not None:
                return pipeline_func(client[database][collection], shard_match=match, schema=schema, **kwargs)

            return aggregate_arrow_all(
                client[database][collection], match + pipeline, schema=schema, **kwargs
            )
        
        def _to_mongo_uri(uri_info: Dict) -> str:
            nodelist = uri_info.get('nodelist', [])
            username = uri_info.get('username', None)
            password = uri_info.get('password', None)
            database = uri_info.get('database', None)
            collection = uri_info.get('collection', None)
            options = uri_info.get('options', {})
            fqdn = uri_info.get('fqdn', None)

            host_port_str = ",".join(nodelist)

            credentials_str = ''
            if username is not None and password is not None:
                credentials_str = f"{username}:{password}@"

            db_collection_str = ''
            if database is not None and collection is not None:
                db_collection_str = f"/{database}/{collection}"

            options_str = ''
            if options:
                options_str = "?" + "&".join([f"{key}={value}" for key, value in options.items()])

            if fqdn is not None:
                args = "retryWrites=false&tls=true&tlsAllowInvalidCertificates=false&tlsAllowInvalidHostnames=false"
                mongo_uri = f"mongodb+srv://{credentials_str}{host_port_str}/{db_collection_str}{options_str}?{args}"
            else:
                mongo_uri = f"mongodb://{credentials_str}{host_port_str}/{db_collection_str}{options_str}"

            return mongo_uri

        self._get_or_create_client()
        coll = self._client[self._database][self._collection]
        match_query = self._get_match_query(self._pipeline)
        
        config_database = self._client["config"]
        config_collections = config_database["collections"]
        config_collection_metadata = config_collections.find_one(
            filter={'_id': f"{self._database}.{self._collection}"})

        if config_collection_metadata is None:
            raise ValueError(f"{self._collection} is not sharded, please use precise parallelism")

        if config_collection_metadata["dropped"]:
            raise ValueError(f"{self._collection} has been dropped, please use precise parallelism")

        key_doc = config_collection_metadata["key"]
        if len(key_doc) > 1:
            raise ValueError("Invalid partitioner strategy. The Sharded partitioner does not support compound "
                                "shard keys.")
        elif "hashed" in key_doc.values():
            raise ValueError("Invalid partitioner strategy. The Sharded partitioner does not support hashed shard "
                                "keys.")

        ns_condition = {"ns": config_collection_metadata["_id"]}
        uuid_condition = {"uuid": config_collection_metadata["uuid"]}
        chunk_collections = config_database["chunks"]
        chunks = [chunk for chunk in
                    chunk_collections.find({'$or': [ns_condition, uuid_condition]},
                                            projection={"min": True, "max": True, "shard": True})
                    .sort("min", pymongo.ASCENDING)]

        shard_map = {}
        for shard in config_database["shards"].find({}, projection={"_id": True, "host": True}):
            host_ports = []
            for host_port in shard["host"].split(','):
                host_ports.append(host_port.split('/')[-1])

            shard_map[shard["_id"]] = host_ports

        # input partition has two element, first is query condition, second is shard host list
        input_partitions = []
        for chunk in chunks:
            chunk_min = chunk["min"]
            chunk_max = chunk["max"]
            # chunk min size must equals chunk max size
            query_condition = {}
            for key in chunk_min.keys():
                query_condition[key] = {
                    '$gte': chunk_min.get(key, bson.min_key),
                    '$lt': chunk_max.get(key, bson.max_key)
                }

            shard = chunk["shard"]
            input_partitions.append((query_condition, shard_map[shard]))

        read_tasks: List[ReadTask] = []
        for i, input_partition in enumerate(input_partitions):
            count_result = list(coll.aggregate(
                [
                    {"$match": {'$and': [match_query, input_partition[0]]}},
                    {'$group': {'_id': None, 'count': {'$sum': 1}}}
                ],
                allowDiskUse=True,
            ))
            count = count_result[0]['count'] if count_result else 0
            metadata = BlockMetadata(
                num_rows=count,
                size_bytes=int(count * self._avg_obj_size),
                schema=None,
                input_files=None,
                exec_stats=None,
            )
            make_shard_block_args = (
                self._uri,
                self._database,
                self._collection,
                self._pipeline,
                self._pipeline_func,
                input_partition[0],
                input_partition[1],
                self._schema,
                self._mongo_args,
            )

            read_task = ReadTask(
                lambda args=make_shard_block_args: [make_block(*args)],
                metadata,
            )
            read_tasks.append(read_task)
        return read_tasks


def _example_read(item):
    """Example for reading data from ShardedMongoDatasource."""
    name = item["name"]
    float_field = item["float_field"]
    int_field = item["int_field"]
    print(f"name: {name}, float_field: {float_field}, int_field: {int_field}")

    return {
        "name": name,
        "float_field": float_field,
        "int_field": int_field
    }

import ray

@ray.remote
def _example_pipeline():
    """Example for using ShardedMongoDatasource by mongo pipeline."""
    from ray.data.read_api import read_datasource
    from pymongoarrow.api import Schema
    import pyarrow as pa

    uri = "mongodb://root:mongo123#@10.27.240.45:8719"
    db_name = "lyw"
    collection_name = "test"
    schema = Schema({"name": pa.string(), "float_field": pa.float64(), "int_field": pa.int32()})

    source = ShardedMongoDatasource(
        uri=uri,
        database=db_name,
        collection=collection_name,
        pipeline=[{ "$match": { "name": { "$exists": True } } }],
        schema=schema)
    ds = read_datasource(source, parallelism=10)

    ds = ds.map(_example_read)
    ds.show(1)

@ray.remote
def _example_pipeline_func():
    """Example for using ShardedMongoDatasource by custom pipeline function."""
    from ray.data.read_api import read_datasource
    from pymongoarrow.api import Schema
    import pyarrow as pa

    uri = "mongodb://root:mongo123#@10.27.240.45:8719"
    db_name = "lyw"
    collection_name = "test"
    schema = Schema({"name": pa.string(), "float_field": pa.float64(), "int_field": pa.int32()})

    def pipeline_func(collection, shard_match, schema=None, **kwargs):
        from pymongoarrow.api import aggregate_arrow_all

        pipeline = [{ "$match": { "name": { "$exists": True } } }]
        return aggregate_arrow_all(collection, shard_match + pipeline, schema=schema, **kwargs)

    source = ShardedMongoDatasource(
        uri=uri,
        database=db_name,
        collection=collection_name,
        pipeline_func=pipeline_func,
        schema=schema)
    ds = read_datasource(source, parallelism=10)

    ds = ds.map(_example_read)
    ds.show(1)


if __name__ == "__main__":
    ray.init(address="ray://10.27.240.45:8887")
    ray.get(_example_pipeline.remote())
    ray.get(_example_pipeline_func.remote())
    ray.shutdown()