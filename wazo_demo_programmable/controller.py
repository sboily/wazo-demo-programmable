# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import signal

from functools import partial
from xivo import plugin_helpers

from . import websocket
from .http_server import CoreHTTP
from .thread_manager import ThreadManager


logger = logging.getLogger(__name__)


class Controller:

    def __init__(self, config):
        self.server = CoreHTTP(config)
        self.websocket_consumer = websocket.Consumer(config)
        self.thread_manager = ThreadManager()
        plugin_helpers.load(
            namespace='wazo_demo_programmable.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'config': config,
                'websocket_consumer': self.websocket_consumer,
                'flask': self.server.get_app(),
            }
        )

    def run(self):
        logger.info('wazo-demo-programmable starting...')
        signal.signal(signal.SIGTERM, partial(_sigterm_handler, self))
        with self.thread_manager:
            with websocket.consumer_thread(self.websocket_consumer):
                self.server.run()

    def stop(self, reason):
        logger.warning('Stopping wazo-demo-programmable: %s', reason)
        self.server.stop()


def _sigterm_handler(controller, signum, frame):
    controller.stop(reason='SIGTERM')
