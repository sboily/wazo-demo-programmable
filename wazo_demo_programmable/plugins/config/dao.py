# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .models import (
    Config,
)
from ...plugin_helpers.db import get_dao_session

class ConfigDAO:

    @property
    def session(self):
        return get_dao_session()

    def list_(self):
        return self.session.query(Config).all()

    def create(self, config):
        self.session.add(config)
        self.session.flush()
        return config
