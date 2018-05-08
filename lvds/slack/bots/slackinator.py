#!/usr/bin/env python

from lvds.slack.listen import SlackListen
from pykinator.core import Pykinator

import datetime, os, requests, sys, time


class Slackinator(SlackListen):

    users = {}

    def __init__(self, username='slackinator'):

        if username is None:
            raise AttributeError("which username should we use with Slack?")

        SlackListen.__init__(self, username, run=True)


    def response(self, command=None, output=None):

        user = output['user']

        if user in self.users:
            pk = self.users[user]
            if not pk.game_over:
                if pk.guessing:
                    return pk.guess(command)

                if command in ["quit","exit","stop","q"]:
                    del self.users[user]
                    return("goodbye.")
                elif command in ["guess","done"]:
                    pk.guessing = True
                    return pk.guess()

                return pk.answer(command)
            else:
                del self.users[user]
                return "Let me know when you're ready to play again"
        else:
            self.users[user] = Pykinator()
            return ("Hello, let's play a game I stole from akinator.com\n"
                    "Your mission is to pick character. They can be real "
                    "or from a movie, comic or game.\n"
                    ":sunglasses:\n"
                    "I will ask you a series of questions and eventually "
                    "make a guess. You can force me to make a guess by "
                    "just typing *guess* or you can quit the game by "
                    "typing *quit*. When you're ready here's the first "
                    "question.\n\n{}".format(self.users[user].start()))


if __name__ == "__main__":

    print("What's your bots name? ")
    bot = input("> ")

    print("starting slackinator.\n\n[press ctrl-c to quit]\n")

    try:
        Slackinator(bot)
    except KeyboardInterrupt:
        print("\nshutting down")
