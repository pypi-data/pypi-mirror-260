#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
@File    :   annotation_datasink.py
"""
from typing import List, Union, Iterator, Dict, Tuple, Optional
from windmillcomputev1.filesystem.blobstore import S3BlobStore
from windmillartifactv1.client.artifact_client import ArtifactClient
from windmilltrain.client.training_client import TrainingClient
import logging
import os


class FileDataSink(object):
    """
    FileDataSink
    """
    def __init__(self,
                 s3_bucket: str,
                 bs: S3BlobStore,
                 artifact_client: ArtifactClient = None,
                 train_client: TrainingClient = None,
                 ):
        self.s3_bucket = s3_bucket
        self.bs = bs
        self.artifact_client = artifact_client
        self.train_client = train_client

    def create_location(self, object_name: str):
        """
        create location
        :param object_name:
        :return:
        """
        # 创建位置
        location_resp = self.artifact_client.create_location(
            object_name=object_name
        )
        return location_resp

    def upload_file(self, source_path: str, dest_path: str):
        """
        upload file to s3
        :param source_path:
        :param dest_path:
        :return:
        """
        self.bs.upload_file(source_path, dest_path)

    def write_file(self, data, dest_path: str):
        """
        write file to s3
        :param data:
        :param dest_path:
        :return:
        """
        self.bs.write_file(dest_path, data)

    def create_dataset(self, location_resp, common_dict: Union[Dict]):
        """
        create dataset
        :param location_resp:
        :param common_dict:
        :return:
        """
        # 创建数据集
        artifact = common_dict.get('artifact', {})
        dataset_resp = self.train_client.create_dataset(
            workspace_id=common_dict.get("workspace_id"),
            project_name=common_dict.get("project_name"),
            category=common_dict.get("category", "Image/ObjectDetection"),
            local_name=common_dict.get("localName"),
            artifact_uri=location_resp.location,
            description=common_dict.get('description', ''),
            display_name=common_dict.get('displayName', ''),
            data_type=common_dict.get('dataType', 'Image'),
            annotation_format=common_dict.get('annotation_format', 'Image'),
            artifact_description=artifact.get('description', ''),
            artifact_alias=artifact.get('alias', []),
            artifact_tags=artifact.get('tags', []),
            artifact_metadata={'paths': [location_resp.location + "/"]},
        )
        logging.info("create dataset resp is {}".format(dataset_resp))