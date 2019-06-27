# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_demo_programmable.plugin_helpers.client import get_auth_client_from_config
from wazo_demo_programmable.plugin_helpers.client import get_calld_client_from_config


class CallService:

    def __init__(self, config):
        self.config = config

    def make_call(self, data):
        calld = get_calld_client_from_config(token=self._get_token(), **self.config['calld'])
        application_uuid = data['application_uuid']
        channel = data['call']
        call_id = channel['id']
        exten = channel['dialed_extension']
        callerid = channel['caller_id_number']
        context = wazo.config['context']

        node = calld.applications.create_node(application_uuid, [call_id,])
        call = {
            'autoanswer': False,
            'context': context,
            'exten': exten,
            'variables': {'callerId': callerid, 'WAZO_IS_ORIGINATE': 'originate'} # Remove this variable ...
        }
        calld.applications.make_call_to_node(application_uuid, node['uuid'], call)

    def answer_call(self, application_uuid, call_id):
        calld = get_calld_client_from_config(token=self._get_token(), **self.config['calld'])
        calld.applications.answer_call(application_uuid, call_id)

    def _get_token(self):
        auth = get_auth_client_from_config(**self.config['auth'])
        token_data = auth.token.new(expiration=30)
        return token_data.get('token')
