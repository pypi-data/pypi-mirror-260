import logging

import click

from biolib._internal.data_record import DataRecord
from biolib.biolib_logging import logger, logger_no_user_data
from biolib.typing_utils import Optional


@click.group(help='Manage Data Records')
def data_record() -> None:
    pass


@data_record.command(help='Create a Data Record')
@click.option('--destination', type=str, required=True)
@click.option('--data-path', required=True, type=click.Path(exists=True))
@click.option('--name', type=str, required=False)
def create(destination: str, data_path: str, name: Optional[str] = None) -> None:
    logger.configure(default_log_level=logging.INFO)
    logger_no_user_data.configure(default_log_level=logging.INFO)
    DataRecord.create(destination, data_path, name)


@data_record.command(help='Save files from a Data Record')
@click.argument('uri', required=True)
@click.option('--output-dir', required=True, type=click.Path(exists=False))
def save_files(uri: str, output_dir: str) -> None:
    logger.configure(default_log_level=logging.INFO)
    logger_no_user_data.configure(default_log_level=logging.INFO)
    DataRecord(uri).save_files(output_dir)
