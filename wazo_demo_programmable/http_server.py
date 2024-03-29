# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os

from datetime import timedelta

from cheroot import wsgi
from flask import Flask
from flask_cors import CORS
from xivo import http_helpers


VERSION = 1.0

logger = logging.getLogger(__name__)
app = Flask('wazo-demo-programmable')


class CoreHTTP:

    def __init__(self, global_config):
        self.config = global_config['http']
        http_helpers.add_logger(app, logger)
        app.before_request(http_helpers.log_before_request)
        app.after_request(http_helpers.log_request)
        app.secret_key = os.urandom(24)
        app.config.update(global_config)
        app.permanent_session_lifetime = timedelta(minutes=5)
        self._load_cors()
        self.server = None

    def get_app(self):
        return app

    def _load_cors(self):
        cors_config = dict(self.config.get('cors', {}))
        enabled = cors_config.pop('enabled', False)
        if enabled:
            CORS(app, **cors_config)

    def run(self):
        bind_addr = (self.config['listen'], self.config['port'])

        wsgi_app = wsgi.WSGIPathInfoDispatcher({'/': app})
        self.server = wsgi.WSGIServer(bind_addr=bind_addr, wsgi_app=wsgi_app)
        self.server.ssl_adapter = http_helpers.ssl_adapter(
            self.config['certificate'],
            self.config['private_key']
        )
        logger.debug(
            'WSGIServer starting... uid: %s, listen: %s:%s',
            os.getuid(),
            bind_addr[0],
            bind_addr[1]
        )
        for route in http_helpers.list_routes(app):
            logger.debug(route)

        try:
            self.server.start()
        except KeyboardInterrupt:
            self.server.stop()

    def stop(self):
        if self.server:
            self.server.stop()
