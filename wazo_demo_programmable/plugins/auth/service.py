# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ...plugin_helpers.client import get_auth_client_from_config


class AuthService:

    def __init__(self, config):
        self.config = config

    def get_auth(self, username, password):
        auth = get_auth_client_from_config(**self.config['auth'], username=username, password=password)
        token = auth.token.new(expiration=3600)
        return str({
            'token': token.get('token'),
            'user_uuid': token.get('metadata').get('uuid')
        })

    def revoke(self, token):
        auth = get_auth_client_from_config(**self.config['auth'], token=token)
        token = auth.token.revoke(token)
        return str(token)
