# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from .models import Config


class ConfigService:

    def __init__(self, config, dao):
        self.config = config
        self.dao = dao

    def set_config(self, number, user_uuid):
        config = Config()
        config.number = number
        config.user_uuid = user_uuid
        return str(self.dao.create(config))

    def get_configs(self):
        return str(self.dao.list_())
