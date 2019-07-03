# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from ...plugin_helpers.client import get_auth_client_from_config


class AuthService:

    def __init__(self, config):
        self.config = config['auth']

    def get_auth(self, username, password):
        config = {
            'host': self.config['host'],
            'port': self.config['port'],
            'prefix': self.config['prefix'],
        }
        auth = get_auth_client_from_config(**config, username=username, password=password)
        try:
            token = auth.token.new(expiration=3600)
            return json.dumps({
                'token': token.get('token'),
                'user_uuid': token.get('metadata').get('uuid')
            })
        except Exception as e:
            return json.dumps({
                'error': str(e)
            })

    def revoke(self, token):
        auth = get_auth_client_from_config(**self.config, token=token)
        token = auth.token.revoke(token)
        return str(token)
