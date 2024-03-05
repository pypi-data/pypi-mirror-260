import os
from datetime import datetime

from biolib import lfs
from biolib.typing_utils import Optional


class DataRecord:

    def __init__(self, uri: str):
        self._uri = uri

    @property
    def uri(self) -> str:
        return self._uri

    @staticmethod
    def create(destination: str, data_path: str, name: Optional[str] = None) -> 'DataRecord':
        assert os.path.isdir(data_path), f'The path "{data_path}" is not a directory.'
        record_name = name if name else 'data-record-' + datetime.now().isoformat().split('.')[0].replace(':', '-')
        record_uri = lfs.create_large_file_system(lfs_uri=f'{destination}/{record_name}')
        record_version_uri = lfs.push_large_file_system(lfs_uri=record_uri, input_dir=data_path)
        return DataRecord(uri=record_version_uri)
