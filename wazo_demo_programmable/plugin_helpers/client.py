# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import g
from werkzeug.local import LocalProxy

from wazo_auth_client import Client as AuthClient
from wazo_calld_client import Client as CalldClient


def get_auth_client_from_config(**config):
    client = AuthClient(
        **config
    )
    return client

def get_calld_client_from_config(token, **config):
    client = CalldClient(
        token=token,
        **config
    )
    return client
