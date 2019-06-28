# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import request
from flask_classful import FlaskView


class AuthResource(FlaskView):

    def index(self):
        param = request.args
        username = param.get('username')
        password = param.get('password')
        return self.service.get_auth(username, password)

    def logout(self, token):
        return self.service.revoke(token)
