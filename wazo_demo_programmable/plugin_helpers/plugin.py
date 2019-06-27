# Copyright 2019 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import Blueprint


def create_blueprint(name, import_name, url_prefix=None):
    return Blueprint(name, import_name, static_url_path='/%s' % import_name, url_prefix=url_prefix)
