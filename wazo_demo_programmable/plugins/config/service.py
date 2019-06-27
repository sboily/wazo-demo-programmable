# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ConfigService:

    def __init__(self, config):
        self.config = config
        self.pbx_config = dict()

    def set_config(self, number, user_uuid):
        self.pbx_config[number] = user_uuid
        return str(self.pbx_config[number])

    def get_configs(self):
        return str(self.pbx_config)
