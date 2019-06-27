# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

logger = logging.getLogger(__name__)


class WsEventHandler:

    def __init__(self, service):
        self._service = service

    def subscribe(self, ws_consumer):
        ws_consumer.on_event('application_call_entered', self._application_call_entered)
        ws_consumer.on_event('application_node_updated', self._application_node_updated)

    def _application_call_entered(self, event):
        self._service.incoming_call(event)

    def _application_node_updated(self, data):
        application_uuid = data['application_uuid']
        calls = data['node']['calls']
        if len(calls) > 1:
            call_id = data['node']['calls'][0]['id']
            self._service.answer_call(application_uuid, call_id)
