#!/usr/bin/env python

"""
Make Your Own Slackbot

This module gives you two ways of creating your own slackbot.

EXAMPLES:

1. Script

slack = SlackListen('myrobot')
while slack.connected:
    query, output = slack.question()
    response = # my generated response
    slack.answer(response, output)

2. Object

#just override the 'response' method

class MyRobot(SlackListen):

    def response(self, command=None, output=None):
        return "Did you say? `%s`".format(command)

# Then in your script set the run attribute

MyRobot('myrobot', run=True)
"""

from lvds.slack.connect import SlackConnect

import sys, time

class SlackListen(SlackConnect):

    READ_WEBSOCKET_DELAY = 1

    slack_username = ''
    slack_bot_id = ''

    script = True

    def __init__(self, username=None, run=False):
        if username is None:
            raise AttributeError("which username should we use with Slack?")

        SlackConnect.__init__(self, username)

        self.set_bot_id()

        if run:
            self.script = False
            self.run()


    def run(self):
        while True:
            command, output = self.parse_slack_output(self.sc.rtm_read())

            if command and 'channel' in output and output['channel']:
                if self.script:
                    return (command, output)
                else:
                    self.handle_command(command, output)

            time.sleep(self.READ_WEBSOCKET_DELAY)


    def question(self):
        """
        Incoming question
        (for use in scripts)
        """
        self.run()


    def answer(self, response="can you repeat that?", output=None):
        """
        Outgoing response
        (for use in scripts)
        """
        if output is None:
            raise AttributeError("output can't be empty")

        self.handle_command(response, output)


    def set_bot_id(self):
        api_call = self.sc.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.username:
                    self.slack_bot_id = user.get('id')
                    return

        print("could not find bot user with name: " + self.username)


    def handle_command(self, command, output):

        if command and 'channel' in output:
            response = self.response(command, output)

            self.sc.api_call("chat.postMessage", channel=output['channel'],
                text=response, as_user=True)


    def parse_slack_output(self, output_list=None):

        at_bot = '<@'+self.slack_bot_id+'>'

        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and \
                  'user' in output and output['user'] != self.slack_bot_id:
                    command = output['text']
                    if command.startswith(at_bot):
                        command = command.split(at_bot)[1].strip().lower()

                    return command, output

        return None, None


    # overwrite this in your robot libs
    def response(self, command=None, output=None):
        return "I don't know what to do with: %s" % command


if __name__ == "__main__":

    print("if everything worked, the little button next to your app "
          "should turn green showing that you're online\n\n"
          "Press <ctrl-c> to quit")
    
    sm = SlackListen('lexibot', run=True)

