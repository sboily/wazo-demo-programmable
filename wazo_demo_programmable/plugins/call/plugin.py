# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .websocket_consume import WsEventHandler
from .service import CallService


class Plugin:

    def load(self, dependencies):
        config = dependencies['config']
        ws_consumer = dependencies['websocket_consumer']

        service = CallService(config)

        ws_event_handler = WsEventHandler(service)
        ws_event_handler.subscribe(ws_consumer)
