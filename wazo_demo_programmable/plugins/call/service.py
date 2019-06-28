# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import requests

from ...plugin_helpers.client import get_auth_client_from_config
from ...plugin_helpers.client import get_calld_client_from_config
from ...plugin_helpers.client import get_confd_client_from_config


class CallService:

    def __init__(self, config):
        self.config = config

    def incoming_call(self, data):
        dialed_extension = data['call']['dialed_extension']
        config = self._get_config(dialed_extension)
        if config:
            exten, context = self._user_extension_context(config['user_uuid'])
            print('Call extension {} in context {}'.format(exten, context))
            self._make_call_with_extension(data, exten, context)
        else:
            print('There is no configuration for this number')
            self.hangup_call(data)

    def hangup_call(self, data):
        calld = get_calld_client_from_config(token=self._get_token(), **self.config['calld'])
        application_uuid = data['application_uuid']
        call_id = data['call']['id']
        calld.applications.hangup_call(application_uuid, call_id)

    def node_updated(self, data):
        application_uuid = data['application_uuid']
        calls = data['node']['calls']
        if len(calls) > 1:
            print('There is two channels inside the node, start the conversation...')
            call_id = data['node']['calls'][0]['id']
            self._service.answer_call(application_uuid, call_id)
        elif len(calls) == 1:
            print('There is a channel inside the node, waiting for a second...')
        else:
            print('Node is now empty and it will been removed')

    def answer_call(self, application_uuid, call_id):
        calld = get_calld_client_from_config(token=self._get_token(), **self.config['calld'])
        calld.applications.answer_call(application_uuid, call_id)

    def _get_token(self):
        auth = get_auth_client_from_config(**self.config['auth'])
        token_data = auth.token.new(expiration=30)
        return token_data.get('token')

    def _get_config(self, extension):
        configs = self._get_configs()
        for config in configs:
            if config['number'] == extension:
                return config
        return None

    def _user_extension_context(self, user_uuid):
        user = self._search_user(user_uuid)
        if user:
            extensions = user['lines'][0]['extensions']
            return (extensions[0]['exten'], extensions[0]['context'])

    def _search_user(self, user_uuid):
        print('Search user {}...'.format(user_uuid))
        confd = get_confd_client_from_config(token=self._get_token(), **self.config['confd'])
        return confd.users.get(user_uuid)

    def _make_call_with_extension(self, data, exten, context):
        calld = get_calld_client_from_config(token=self._get_token(), **self.config['calld'])
        application_uuid = data['application_uuid']
        channel = data['call']
        call_id = channel['id']
        exten = exten or channel['dialed_extension']
        callerid = channel['caller_id_number']
        context = context

        node = calld.applications.create_node(application_uuid, [call_id,])
        print('Creating node conversation: {}'.format(node))
        call = {
            'autoanswer': False,
            'context': context,
            'exten': exten,
            'variables': {'callerId': callerid, 'WAZO_IS_ORIGINATE': 'originate'} # Remove this variable ...
        }
        chan = calld.applications.make_call_to_node(application_uuid, node['uuid'], call)
        print('Add new channel to the conversation: {}'.format(chan))


    def _get_configs(self):
        r = requests.get("https://localhost:9400/config/list/", verify=False)
        return json.loads(r.text)
