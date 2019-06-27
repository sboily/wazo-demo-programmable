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
        if self._search(config.number):
            return False

        self.session.add(config)
        self.session.commit()
        return True

    def delete(self, id):
        config = self.session.query(Config).filter(Config.id == id).first()
        if config:
            self.session.delete(config)
            self.session.commit()
            return True
        return False

    def _search(self, number):
        search = self.session.query(Config).filter(Config.number == number).first()
        if search:
            return True
        return False
