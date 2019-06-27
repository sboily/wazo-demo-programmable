# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from contextlib import contextmanager
from threading import Thread

from wazo_websocketd_client import Client as Websocketd

logger = logging.getLogger(__name__)


@contextmanager
def consumer_thread(consumer):
    thread_name = 'websocket_consumer_thread'
    thread = Thread(target=consumer.run, name=thread_name)
    thread.start()
    try:
        yield
    finally:
        logger.debug('stopping websocket consumer thread')
        consumer.stop()
        logger.debug('joining websocket consumer thread')
        thread.join()


class Consumer():

    def __init__(self, global_config):
        self.config = global_config['websocketd']
        self._is_running = False
        self._callbacks = {}

    def run(self):
        logger.info("Running WEBSOCKET consumer")
        token = '03ade0f5-00bf-4ba4-bdef-b1fed1a636b8'
        ws = Websocketd(self.config['host'], token=token, verify_certificate=False)
        self._run_ws(ws)

    def _run_ws(self, ws):
        for event in self._callbacks:
            ws.on(event, self._callbacks[event])
        ws.run()

    def is_running(self):
        return self._is_running

    def on_event(self, event_name, callback):
        self._callbacks[event_name] = callback

    def stop(self):
        self.should_stop = True
