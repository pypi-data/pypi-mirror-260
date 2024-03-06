import os
from collections import namedtuple
from datetime import datetime
from struct import Struct

from biolib import lfs
from biolib._internal.http_client import HttpClient
from biolib.biolib_api_client import AppGetResponse
from biolib.biolib_api_client.lfs_types import LargeFileSystemVersion
from biolib.biolib_logging import logger
from biolib.typing_utils import Optional, List, Dict, Union
from biolib.api import client as api_client
from biolib.utils.app_uri import parse_app_uri
from biolib.utils.zip.remote_zip import RemoteZip  # type: ignore


class DataRecord:

    def __init__(self, uri: str):
        self._uri = uri

    @property
    def uri(self) -> str:
        return self._uri

    def save_files(self, output_dir: str) -> None:
        app_response: AppGetResponse = api_client.get(path='/app/', params={'uri': self._uri}).json()
        app_version = app_response['app_version']
        lfs_version: LargeFileSystemVersion = api_client.get(path=f"/lfs/versions/{app_version['public_id']}/").json()
        zip_url = lfs_version['presigned_download_url']

        with RemoteZip(zip_url) as remote_zip:
            central_directory = remote_zip.get_central_directory()
            for file in central_directory.values():
                self._download_file(zip_url, file, output_dir)

    @staticmethod
    def create(destination: str, data_path: str, name: Optional[str] = None) -> 'DataRecord':
        assert os.path.isdir(data_path), f'The path "{data_path}" is not a directory.'
        record_name = name if name else 'data-record-' + datetime.now().isoformat().split('.')[0].replace(':', '-')
        record_uri = lfs.create_large_file_system(lfs_uri=f'{destination}/{record_name}')
        record_version_uri = lfs.push_large_file_system(lfs_uri=record_uri, input_dir=data_path)
        return DataRecord(uri=record_version_uri)

    @staticmethod
    def fetch(uri: Optional[str] = None, count: Optional[int] = None) -> List['DataRecord']:
        max_page_size = 1_000
        params: Dict[str, Union[str, int]] = {
            'page_size': str(count or max_page_size),
            'type': 'data-record',
        }
        if uri:
            uri_parsed = parse_app_uri(uri, use_account_as_name_default=False)
            params['account_handle'] = uri_parsed['account_handle_normalized']

        results = api_client.get(path='/apps/', params=params).json()['results']
        if count is None and len(results) == max_page_size:
            logger.warning(
                f'Fetch results exceeded maximum count of {max_page_size}. Some data records might not be fetched.'
            )

        return [DataRecord(result['resource_uri']) for result in results]

    def _download_file(self, zip_url: str, file: Dict, output_dir: str) -> None:
        local_file_header_signature_bytes = b'\x50\x4b\x03\x04'
        local_file_header_struct = Struct('<H2sHHHIIIHH')
        LocalFileHeader = namedtuple('LocalFileHeader', (
            'version',
            'flags',
            'compression_raw',
            'mod_time',
            'mod_date',
            'crc_32_expected',
            'compressed_size_raw',
            'uncompressed_size_raw',
            'file_name_len',
            'extra_field_len',
        ))

        local_file_header_start = file['header_offset'] + len(local_file_header_signature_bytes)
        local_file_header_end = local_file_header_start + local_file_header_struct.size

        local_file_header_response = HttpClient.request(
            url=zip_url,
            headers={'range': f'bytes={local_file_header_start}-{local_file_header_end - 1}'},
            timeout_in_seconds=300,
        )
        local_file_header = LocalFileHeader._make(
            local_file_header_struct.unpack(local_file_header_response.content),
        )

        file_start = local_file_header_end + local_file_header.file_name_len + local_file_header.extra_field_len
        file_end = file_start + file['file_size']

        response = HttpClient.request(
            url=zip_url,
            headers={'range': f'bytes={file_start}-{file_end - 1}'},
            timeout_in_seconds=300,  # timeout after 5 min
        )

        file_path = os.path.join(output_dir, file['filename'])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode='wb') as file_handle:
            file_handle.write(response.content)
