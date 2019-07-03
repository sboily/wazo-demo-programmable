# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

logger = logging.getLogger(__name__)


class WsEventHandler:

    def __init__(self, service):
        self._service = service

    def subscribe(self, ws_consumer):
        ws_consumer.on_event('application_call_entered', self._application_call_entered)
        ws_consumer.on_event('application_user_outgoing_call_created', self._application_user_outgoing_call_created)
        ws_consumer.on_event('application_node_updated', self._application_node_updated)
        ws_consumer.on_event('call_updated', self._data)
        ws_consumer.on_event('call_created', self._data)
        ws_consumer.on_event('call_ended', self._data)

    def _application_call_entered(self, event):
        self._service.incoming_call(event)

    def _application_node_updated(self, event):
        self._service.node_updated(event)

    def _application_user_outgoing_call_created(self, event):
        self._service.outgoing_call(event)

    def _data(self, event):
        print(event)
