# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

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

    def delete_config(self, id):
        self.dao.delete(id)
        return id

    def get_configs(self):
        res = []
        configs = self.dao.list_()
        for config in configs:
            res.append({
                "id": config.id,
                "number": config.number,
                "user_uuid": config.user_uuid
            })
        return json.dumps(res)
