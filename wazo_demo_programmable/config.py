# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import os

from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy, parse_config_file
from xivo.xivo_logging import get_log_level_by_name

_CERT_FILE = '/usr/share/xivo-certs/server.crt'
_DEFAULT_HTTPS_PORT = 9400
_PID_DIR = '/var/run/wazo-demo-programmable'

_DEFAULT_CONFIG = {
    'config_file': '/etc/wazo-demo-programmable/config.yml',
    'debug': False,
    'extra_config_files': '/etc/wazo-demo-programmable/conf.d',
    'log_file': '/var/log/wazo-demo-programmable.log',
    'log_level': 'info',
    'pid_file': os.path.join(_PID_DIR, 'wazo-demo-programmable.pid'),
    'user': 'wazo-demo-programmable',
    'http': {
        'listen': '0.0.0.0',
        'port': _DEFAULT_HTTPS_PORT,
        'certificate': _CERT_FILE,
        'private_key': '/usr/share/xivo-certs/server.key',
    },
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'verify_certificate': _CERT_FILE,
        'key_file': '/var/lib/wazo-auth-keys/wazo-demo-programmable-key.yml',
    },
    'calld': {
        'host': 'localhost',
        'port': 9500,
        'verify_certificate': _CERT_FILE,
    },
    'enabled_plugins': {
        'auth': True,
        'config': True,
        'call': True,
    },
}


def load_config(args):
    cli_config = _parse_cli_args(args)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(cli_config, file_config, _DEFAULT_CONFIG)
    service_key = _load_key_file(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    return ChainMap(reinterpreted_config, cli_config, service_key, file_config, _DEFAULT_CONFIG)


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    if not key_file:
        return {}
    return {'auth': {'username': key_file['service_id'], 'password': key_file['service_key']}}


def _get_reinterpreted_raw_values(*configs):
    config = ChainMap(*configs)
    return dict(
        log_level=get_log_level_by_name('debug' if config['debug'] else config['log_level']),
    )


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', action='store', help='The path to the config file')
    parser.add_argument('-d', '--debug', action='store_true', help='Log debug mesages. Override log_level')
    parser.add_argument('-u', '--user', action='store', help='The owner of the process')
    parsed_args = parser.parse_args(argv)

    result = {}
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        result['debug'] = parsed_args.debug
    if parsed_args.user:
        result['user'] = parsed_args.user

    return result
