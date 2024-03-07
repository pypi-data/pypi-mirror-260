import sys
import os
import ssl
import pickle
from websockets.sync.client import connect

import numpy
from tqdm import tqdm

from xflow.feature.types import DatasetComposition, DatasetElement, DatasetElementInfo
from xflow._utils.utils import (PacketHeader, chunker, get_dataset_upload_url,
                                get_pipeline_info)
from xflow._utils.decorators import executor_method
from xflow._private.request_vo import ExportDataset
from xflow._private._constants import STREAM_DATA_SIZE
from xflow._private._types import PacketHeaderType


class Dataset:
    def __init__(self, name: str, desc: str):
        self._name = name
        self._desc = desc
        self.__data: dict[str, numpy.ndarray] = {}
        self.__composition: DatasetComposition | None = None
        self.__label: list = []

    def append(self, element: DatasetElement):
        name = element.name
        dims = list(numpy.shape(element.data))
        type_ = str(element.data)
        desc = element.desc
        feature_names = element.feature_names
        dataset_elem_info = DatasetElementInfo(NAME=name, DIMS=dims, TYPE=type_, DESC=desc, FEATURE_NAMES=feature_names)
        if self.__composition is None:
            self.__composition = DatasetComposition(DATA=[dataset_elem_info])
        else:
            self.__composition.DATA.append(dataset_elem_info)
        self.__data[name] = element.data

    def set_label(self, label: list):
        self.__label = label

    @executor_method
    def save(self):
        project, pipeline, rev, trial, reg_id = get_pipeline_info()
        upload_url = get_dataset_upload_url()
        connect_arg = {"uri": upload_url}
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connect_arg["ssl_context"] = ssl_context
        info_data = ExportDataset(NAME=self._name, PRJ_ID=project, PPLN_ID=pipeline, RVSN=rev, TRIAL=trial,
                                  CMPST=self.__composition.dict(), DESC=self._desc, REG_ID=reg_id).dict()
        ds_data = {"dataset": self.__data}
        ds_data = pickle.dumps(ds_data)
        header = PacketHeader(header_type=PacketHeaderType.DATA_INFO)
        data_info = info_data
        data_info = bytearray(pickle.dumps(data_info))
        data = header.create_packet(data=data_info)
        with connect(**connect_arg) as websocket:
            websocket.send(data)
            message = websocket.recv(1)
            if message != PacketHeaderType.SUCCESS:
                raise RuntimeError
            progress = tqdm(total=len(ds_data), initial=0, ascii=True, file=sys.stdout)
            header = PacketHeader(header_type=PacketHeaderType.DATA)
            try:
                for chunk in chunker(ds_data, STREAM_DATA_SIZE):
                    data = header.create_packet(data=chunk)
                    websocket.send(data)
                    message = websocket.recv(1)
                    if message != PacketHeaderType.SUCCESS:
                        raise RuntimeError
                    progress.update(len(chunk))
                header = PacketHeader(header_type=PacketHeaderType.EOF)
                data = header.create_packet(data=b'')
                websocket.send(data)
            except Exception as exc:
                raise exc
            finally:
                progress.close()
