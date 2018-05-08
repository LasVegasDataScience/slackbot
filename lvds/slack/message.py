#!/usr/bin/env python

from lvds.slack.connect import SlackConnect

import sys


class SlackMsg(SlackConnect):

    default_channel=None

    ignore_interactive = False


    def __init__(self, username=None, default_channel=None):
        if username is None:
            raise AttributeError("which username should we use with Slack?")

        SlackConnect.__init__(self, username)

        if default_channel is not None:
            if default_channel.startswith("@"):
                self.default_channel = self.userid(default_channel[1:])
            else:
                self.default_channel = default_channel


    def userid(self, user=None):

        if user is None:
            raise AttributeError("user can not be empty")

        acct_id = None
        for acct in self.test_connection().api_call("users.list")['members']:
            if 'profile' in acct and \
              acct['profile']['display_name_normalized'] == user:
                  acct_id = acct['id']
                  break

        if acct_id is None:
            raise AttributeError("lookup for {} failed.".format(user))

        for acct in self.test_connection().api_call("im.list")['ims']:
            if acct['user'] == acct_id:
                return acct['id']

        return None


    """
      channel: CHANNEL_ID or #channel or @username
    """
    def msg(self, message, channel=None):

        if message is None:
            if sys.stdout.isatty():
                print("no message means nothing to do")
            return

        sc = self.test_connection()

        if channel is None:
            if self.default_channel is not None:
                channel = self.default_channel
            else:
                channel = '#random'
        elif channel.startswith("@"):
            channel = self.userid(channel[1:])

        ret = None
        if not self.ignore_interactive and sys.stdout.isatty():
            print("SLACK: [%s]: %s" % (channel, message))
        else:
            ret = sc.api_call(
              'chat.postMessage',
              as_user=True,
              channel=channel,
              text=message
            )

        return ret


if __name__ == "__main__":

    defaults = {
      'robot': 'slackinator',
      'channel': '#playground' # for users place an @ in front of the username
                               # i.e. @Steve
    }

    if sys.stdout.isatty():

        print("Since you are running this interactively, you can modify the\n"
          "defaults, however nothing will actually be sent to Slack, instead\n"
          "you will get a notification as to what would have been sent out.\n"
          "\nIf you want to have these tests sent to slack, you need to run\n"
          "it non-interactively, in other words in the background.\n\n"
          "i.e. on unix enter ` | grep test` at the end of your "
          "command.\nThis makes it non-interactive.\n"
          "**This robot must be identified in your slack configuration "
          "file.**\n")

        robot = input("which robot do you want to be sending the messages? "
          "[{}] > ".format(defaults['robot'])
        )

        if len(robot) == 0:
            robot = defaults['robot']

        channel = input("which channel do you want to receive the messages? "
          "[{}] > ".format(defaults['channel'])
        )

        if len(channel) == 0:
            channel = defaults['channel']
    else:
        robot = defaults['robot']
        channel = defaults['channel']


    sm = SlackMsg(robot)
    print(sm.msg("TEST: and here I am", channel))

    sm2 = SlackMsg(robot, channel)
    print(sm2.msg("TEST: using defaults"))
