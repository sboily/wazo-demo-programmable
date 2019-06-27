# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import request
from flask_classful import FlaskView


class ConfigResource(FlaskView):

    def index(self):
        param = request.args
        number = param.get('number')
        user_uuid = param.get('user_uuid')
        return self.service.set_config(number, user_uuid)

    def list(self):
        return self.service.get_configs()

    def remove(self, id):
        return self.service.delete_config(id)
