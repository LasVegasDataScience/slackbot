#!/usr/bin/env python

"""
  USAGE: sample.py --bot <your bots name>

  i.e. sample.py --bot slackinator

  Your bots name is the same name as you entered
  in the configuration file 'conf/slack.ini'
"""

from lvds.slack.listen import SlackListen

import argparse, sys

# Parse from command line
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bot",
  dest = "bot",
  default = None,
  help = "Your Robot's Name"
)
args = parser.parse_args()

bot = args.bot

if bot is None: # give up and ask
    print("Please enter your bot's name: ")
    bot = input('> ')

# the above is just to get the bot name... here's the real code
slackbot = SlackListen(bot)

print("connected")
while slackbot.connected:
    query, output = slackbot.question()

    # YOUR COOL CODE GOES HERE

    if query == "quit":
        print("quitting...")
        slackbot.answer("hanging up... g'bye", output)
        sys.exit()

    slackbot.answer(
      "did you say? `{}`\n"
      "type `quit` and I'll hangup".format(query), output)

print("disconnected.")
