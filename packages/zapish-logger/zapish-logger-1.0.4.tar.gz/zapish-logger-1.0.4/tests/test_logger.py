import os
import pytest
from zapish_logger import file_logger, read_log_file, console_logger, file_and_console_logger
from zapish_logger.logger import LoggingConfig


def test_file_logger(tmp_path):
    d = tmp_path / 'logs'
    d.mkdir()
    path = os.path.join(str(d), 'unit-test.log')
    logger = file_logger(path=path, name='unit-test')
    logger.warning('one')
    logger.error('two')
    logger.info('three')
    logger.debug('four')
    logger.critical('five')


def test_read_log_file(log_data_path):
    data = read_log_file(log_data_path)
    assert len(data) == 4


def test_console_logger():
    logger = console_logger('unit-test')
    logger.warning('one')
    logger.error('two')
    logger.info('three')
    logger.debug('four')
    logger.critical('five')


def test_file_and_console_logger(tmp_path):
    d = tmp_path / 'logs'
    d.mkdir()
    path = os.path.join(str(d), 'unit-test.log')
    logger = file_and_console_logger(path=path, name='unit-test')
    logger.warning('one')
    logger.error('two')
    logger.info('three')
    logger.debug('four')
    logger.critical('five')


def test_get_config_bad():
    obj = LoggingConfig()
    with pytest.raises(KeyError):
        obj.get_config()


def test_add_file_handler_bad():
    obj = LoggingConfig()
    with pytest.raises(ValueError):
        obj.add_file_handler(path='some_path', log_format='bad')

    with pytest.raises(ValueError):
        obj.add_file_handler(path='some_path', level='BAD')


def test_add_console_handler_bad():
    obj = LoggingConfig()
    with pytest.raises(ValueError):
        obj.add_console_handler(log_format='bad')
