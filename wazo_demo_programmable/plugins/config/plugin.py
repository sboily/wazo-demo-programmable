# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ...plugin_helpers.plugin import create_blueprint

from .http import ConfigResource
from .service import ConfigService
from .dao import ConfigDAO


config = create_blueprint('config', __name__)


class Plugin:

    def load(self, dependencies):
        core = dependencies['flask']
        configuration = dependencies['config']

        service = ConfigService(configuration, ConfigDAO())

        ConfigResource.service = service
        ConfigResource.register(config, route_base='/config')

        core.register_blueprint(config)
