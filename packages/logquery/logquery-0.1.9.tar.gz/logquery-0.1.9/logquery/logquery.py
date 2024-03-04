import binascii
import datetime
import decimal
import itertools
import logging
import os
import re
import traceback
import uuid
from logging.handlers import RotatingFileHandler

import pytz

try:
    import sqlparse

    SQLPARSER = True
except ImportError:
    SQLPARSER = False


class LogQuery:
    LOG_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(
        os.environ.get('INSTANCE_HOME', ''))), 'var', 'log')

    def __init__(self):
        _alchemy_log_file = os.path.join(LogQuery.LOG_DIRECTORY, 'sqlalchemy_queries.sql')
        _alchemy_tb_log_file = os.path.join(LogQuery.LOG_DIRECTORY, 'sqlalchemy_tracebacks.sql')
        _zsql_log_file = os.path.join(LogQuery.LOG_DIRECTORY, 'zsql_queries.sql')
        _zsql_tb_log_file = os.path.join(LogQuery.LOG_DIRECTORY, 'zsql_tracebacks.sql')

        self.alchemy_logger = self._setup_logger('sqlalchemy_queries', _alchemy_log_file)
        self.zsql_logger = self._setup_logger('zsql_queries', _zsql_log_file)
        self.alchemy_tb_logger = self._setup_logger('sqlalchemy_tracebacks', _alchemy_tb_log_file)
        self.zsql_tb_logger = self._setup_logger('zsql_tracebacks', _zsql_tb_log_file)

    @staticmethod
    def _setup_logger(name, log_file):
        logging.Formatter.converter = \
            lambda *args: datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')).timetuple()
        logger = logging.getLogger(name)
        logger.propagate = False
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('{0}\n-- %(asctime)s\n%(message)s\n'.format('-' * 100),
                                      '%Y-%m-%d %I:%M:%S %p')
        handler = RotatingFileHandler(filename=log_file, maxBytes=1048576, backupCount=2, encoding='utf-8')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def _quote_simple_value(value):
        if value is None:
            return 'NULL'
        if isinstance(value, bool):
            return '1' if value else '0'
        if isinstance(value, (int, decimal.Decimal, float)):
            return str(value)
        if isinstance(value, uuid.UUID):
            return str(value)
        if isinstance(value, basestring):
            return "'%s'" % value.replace("'", "''")
        if isinstance(value, (bytearray, bytes)):
            return '0x' + binascii.hexlify(bytes(value))
        if isinstance(value, datetime.datetime):
            return "'{0}'".format(value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        if isinstance(value, datetime.date):
            return "'{0}'".format(value.strftime('%Y-%m-%d'))
        if isinstance(value, tuple) and len(value) == 1:
            return LogQuery._quote_simple_value(value[0])
        return None

    def _log_traceback(self, unique_id, zsql_name):
        traceback_info = traceback.extract_stack()[:-2]
        formatted_traceback = traceback.format_list(traceback_info)
        tb_string = ''.join(formatted_traceback)
        if zsql_name:
            self.zsql_tb_logger.info('{0}\n{1}\n{0}\n{2}\n{0}\n'
                                     .format('-' * 100, unique_id, tb_string))
        else:
            self.alchemy_tb_logger.info('{0}\n{1}\n{0}\n{2}\n{0}\n'
                                        .format('-' * 100, unique_id, tb_string))

    def log_query(self, statement, parameters, zsql_name='', log_tb=False):
        unique_id = str(uuid.uuid4())
        statement, parameters = self._get_parameterized_query(statement, parameters, zsql_name)
        statement = self.prettify_query(statement)
        if zsql_name:
            file_name = os.path.basename(zsql_name)
            log_to_write = ('{0}\n-- {1}\n{0}\n-- {2}\n-- {3}\n{0}\n{4}\n{0}\n-- PARAMETERS: {5}\n{0}\n'
                            .format('-' * 100, unique_id, file_name, zsql_name, statement, parameters))
            self.zsql_logger.info(log_to_write)
        else:
            log_to_write = ('{0}\n-- {1}\n{0}\n{2}\n{0}\n-- PARAMETERS: {3}\n{0}\n'
                            .format('-' * 100, unique_id, statement, parameters))
            self.alchemy_logger.info(log_to_write)
        if log_tb:
            self._log_traceback(unique_id, zsql_name)

    def _get_parameterized_query(self, statement, parameters, query_type=''):
        if query_type:
            params = re.findall("<ZESQL-BIND>(.*?)</ZESQL-BIND>", statement, re.I | re.S)
            for param in params:
                statement = statement.replace("<ZESQL-BIND>{}</ZESQL-BIND>".format(param), "'{}'".format(param))
            return statement.strip(), params
        else:
            quoted_params = [self._quote_simple_value(param) for param in parameters]
            statement_list = statement.split('?')
            return ''.join([param for param in itertools.chain.from_iterable(
                itertools.izip_longest(statement_list, quoted_params)) if param]), quoted_params

    @staticmethod
    def prettify_query(query):
        if SQLPARSER:
            return sqlparse.format(sql=query,
                                   reindent=True,
                                   keyword_case='upper',
                                   strip_whitespace=True,
                                   strip_comments=True,
                                   use_space_around_operators=False)
        return query.strip()
