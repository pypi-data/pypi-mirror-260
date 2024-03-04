# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
"""
FileDatasource
"""

import logging
from typing import Dict, Any, Union, List

import ray.data
from windmillcomputev1.filesystem.blobstore import S3BlobStore
import os
from pydantic import BaseModel


logger = logging.getLogger(__name__)

DATA_TYPE_IMAGE = "image"
DATA_TYPE_ANNOTATION = "annotation"
ANNOTATION_TYPE_COCO = "coco"
ANNOTATION_TYPE_VISTUDIO_V1 = "vistudiov1"

image_extensions = ('.jpeg', '.jpg', '.png', '.bmp')


class FileDatasource(object):
    """
    FileDatasource
    """
    def __init__(self,
                 s3_bucket: str = "",
                 bs: S3BlobStore = None,
                 ):
        self.s3_bucket = s3_bucket
        self.bs = bs

    def read_json_file(self, file_uri:  Union[str] = "") -> ray.data.Dataset:
        """
        read_json_file
        :param file_uri:
        :return: ray.data.Dataset
        """
        logger.info("Read Json. Start process file: {}.".format(file_uri))
        ext = os.path.splitext(file_uri)[1].lower()
        if ext == "":
            filenames = self._get_filenames(file_uri, 0, self.s3_bucket, self.bs)
        else:
            filenames = [file_uri]
        file_paths = list()
        for filename in filenames:
            if not filename.lower().endswith('.json'):
                continue

            dest_path = filename[5:]
            self.bs.download_file(filename, dest_path)
            file_paths.append(dest_path)

        ds = ray.data.read_json(file_paths)
        return ds

    def read_image_file(self, file_uri:  Union[str] = "") -> ray.data.Dataset:
        """
        read_image_file
        :return: ray.data.Dataset
        """
        logger.info("From Image. Start process file: {}.".format(file_uri))

        ext = os.path.splitext(file_uri)[1].lower()
        if ext == "":
            filenames = self._get_filenames(file_uri, 2, self.s3_bucket, self.bs)
        else:
            filenames = [file_uri]
        image_list = list()
        for filename in filenames:
            data = {
                "file_uri": filename,
            }
            image_list.append(data)
        # image_list = [Image(fileUri=filename, width=0, height=0) for filename in filenames]
        ds = ray.data.from_items(image_list)

        return ds


    @staticmethod
    def _get_filenames(file_uri, layer, s3_bucket, bs):
        """
        :param file_uri: s3地址
        :param layer: 遍历的层数
        :return: 文件filename列表
        """
        filenames = []
        dest_path = file_uri.split(s3_bucket + '/')[1]
        if not dest_path.endswith("/"):
            dest_path += "/"
        dest_parts = dest_path.split('/')[:-1]

        file_list = bs.list_file(dest_path)
        for file in file_list:
            f_path = file['Key']
            f_parts = f_path.split('/')[:-1]
            # 此处表示取文件夹3层内的数据
            if len(f_parts) - len(dest_parts) > layer:
                continue
            filename = "s3://" + os.path.join(s3_bucket, f_path)
            filenames.append(filename)

        return filenames





from pyarrow.fs import S3FileSystem

S3FileSystem()

