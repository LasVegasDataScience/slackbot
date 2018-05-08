#!/usr/bin/env python

from lvds.config.find_dir import FindDir

from configparser import ConfigParser
from slackclient import SlackClient

import os, time

"""

  We are using test tokens here... this should be updated
    http://slackapi.github.io/python-slackclient/auth.html#test-tokens

"""
class SlackConnect(object):

    sc = None # Slack Client
    username = None
    conf = None

    connected = False
    attempted_connections = 0

    def __init__(self, username=None, conf_file=None):

        if username is None:
            raise AttributeError("username is empty: can't connect")

        if conf_file is None: conf_file = 'slack.ini'

        self.username = username if username is not None \
            else os.getenv('SLACK_USERNAME', False)

        self.conf = ConfigParser()
        self.conf.read(os.path.join(FindDir().conf_dir, conf_file))

        self._build_connection()


    def __del__(self):
        connected = False
        del self.sc
        time.sleep(1)


    def _build_connection(self):

        def sc_connect():
            self.attempted_connections += 1
            self.sc = SlackClient(self.conf[self.username]['SLACK_BOT_TOKEN'])
            self.sc.rtm_connect()

        if self.sc is None:
            time.sleep(self.attempted_connections)
            sc_connect()

        try:
            self.sc.rtm_read()
        except:
            if self.attempted_connections > 9:
                self.connected = False
                del self.sc
                return None

            self.test_connection()

        self.connected = True
        self.attempted_connections = 0 # reset
        return self.sc


    def test_connection(self):
        return self._build_connection()


    def bot_id(self):
        sc = self._build_connection()

        api_call = sc.api_call('users.list')
        if api_call.get('ok'):
            # retrive all users to find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.username:
                    return user.get('id')


if __name__ == "__main__":

    slack = SlackConnect('lexibot')
    print("bot id: ", slack.bot_id())
