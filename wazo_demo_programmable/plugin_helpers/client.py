# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import g
from werkzeug.local import LocalProxy

from wazo_auth_client import Client as AuthClient
from wazo_calld_client import Client as CalldClient
from wazo_confd_client import Client as ConfdClient


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

def get_confd_client_from_config(token, **config):
    client = ConfdClient(
        token=token,
        **config
    )
    return client
