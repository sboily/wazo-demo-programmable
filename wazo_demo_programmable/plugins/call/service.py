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
        self.calld = None

    def outgoing_call(self, data):
        print('Outgoing call..')
        self.calld = get_calld_client_from_config(token=self._get_token(), **self.config['calld'])
        user_uuid = data['call']['user_uuid']
        call_id = data['call']['id']
        application_uuid = data['application_uuid']
        _, context = self._user_extension_context(user_uuid)
        exten = data['call']['dialed_extension']
        print('Call extension {} in context {}'.format(exten, context))
        self.send_progress(application_uuid, call_id)
        self._make_call_with_extension(data, exten, context)

    def incoming_call(self, data):
        print('Incoming call..')
        self.calld = get_calld_client_from_config(token=self._get_token(), **self.config['calld'])
        dialed_extension = data['call']['dialed_extension']
        call_id = data['call']['id']
        application_uuid = data['application_uuid']
        self.send_progress(application_uuid, call_id)
        config = self._get_config(dialed_extension)
        if config:
            self._make_call_with_user_uuid(data, config['user_uuid'])
        else:
            print('There is no configuration for this number')
            self.hangup_call(application_uuid, call_id)

    def call_ended(self, data):
        call_id = data['call_id']
        print('Call ended {}'.format(call_id))

    def send_progress(self, application_uuid, call_id):
        self.calld.applications.start_progress(application_uuid, call_id)

    def hangup_call(self, application_uuid, call_id):
        self.calld.applications.hangup_call(application_uuid, call_id)

    def node_updated(self, data):
        application_uuid = data['application_uuid']
        calls = data['node']['calls']
        if len(calls) > 1:
            print('There is two channels inside the node, start the conversation...')
            call_id = data['node']['calls'][0]['id']
            self.answer_call(application_uuid, call_id)
        elif len(calls) == 1:
            print('There is a channel inside the node, waiting for a second...')
        else:
            print('Node is now empty and it will been removed')

    def answer_call(self, application_uuid, call_id):
        self.calld.applications.answer_call(application_uuid, call_id)

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

    def _make_call_with_extension(self, data, exten, context, user_uuid=None):
        application_uuid = data['application_uuid']
        channel = data['call']
        call_id = channel['id']
        callerid = channel['caller_id_number']

        node = self.calld.applications.create_node(application_uuid, [call_id,])
        print('Creating node conversation: {}'.format(node))
        call = {
            'autoanswer': False,
            'context': context,
            'exten': exten,
            'displayed_caller_id_number': callerid,
        }
        try:
            chan = self.calld.applications.make_call_to_node(application_uuid, node['uuid'], call)
            print('Add new channel to the conversation: {}'.format(chan))
        except:
            print('Error to call this number: {}'.format(exten))
            self.hangup_call(application_uuid, call_id)

    def _make_call_with_user_uuid(self, data, user_uuid):
        application_uuid = data['application_uuid']
        channel = data['call']
        call_id = channel['id']
        callerid = channel['caller_id_number']

        node = self.calld.applications.create_node(application_uuid, [call_id,])
        print('Creating node conversation: {}'.format(node))
        call = {
            'autoanswer': False,
            'user_uuid': user_uuid,
            'displayed_caller_id_number': callerid,
        }
        try:
            chan = self.calld.applications.make_call_user_to_node(application_uuid, node['uuid'], call)
            print('Add new channel to the conversation: {}'.format(chan))
        except Exception as e:
            print('Error to call this user: {}'.format(user_uuid))
            self.hangup_call(application_uuid, call_id)

    def _get_configs(self):
        r = requests.get("https://localhost:9400/config/list/", verify=False)
        return json.loads(r.text)
