# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_demo_programmable.plugin_helpers.plugin import create_blueprint

from .http import AuthResource
from .service import AuthService


auth = create_blueprint('auth', __name__)


class Plugin:

    def load(self, dependencies):
        core = dependencies['flask']
        config = dependencies['config']

        service = AuthService(config)

        AuthResource.service = service
        AuthResource.register(auth, route_base='/auth')

        core.register_blueprint(auth)
