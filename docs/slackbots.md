| [Home](README.md) | [Workspace](workspace.md) | [Slack App](slack_app.md) | *SAMPLES* |
| --- | --- | --- | --- | 


# Slackbots

_simple examples of slackbots and how to create your own_

## Sample

The following sample is provided with almost no functionality to be as boring
as feasible. To run it you simply need to know your bots name. 
_i.e. the name you used in the `conf/slack.ini` file._

```
bin/sample.py --bot myrobot
```

You'll see your bot light up with a green dot next to it and you can send it a
direct message now. It will even reply.

### DETAILS

Most of the code is used to gather up your bot name. Here's the relevant 
portions explained as a mini script

```
from lvds.slack.listen import SlackListen

slackbot = SlackListen('mybot')

while slackbot.connected:
    query, output = slackbot.question()

    slackbot.answer("did you say? `{}`\n".format(query), output)
```

In this case, our bot is called `mybot` and we initialize our object with it.
As long as the bot is connected we wait for a request (_question()_) from the
user over slack. When that happens we reply (_answer()_) and as long as we 
are still connected, wait for another request.

## Slackinator

_a slighly more advanced version_

You don't have to build your Slackbots as scripts, they can be turned into
objects too. *Slackinator* came from the website, 
[Akinator](http://en.akinator.com/). It's like playing 20 questions while 
guessing famous people instead of objects. In this example we use your robot
to link the two so you can play the game over Slack.

*NOTE*

Slackinator requires [pykinator](https://github.com/yxes/pykinator) to run and
currently, there are problems connecting to the Akinator server. Until those
are fixed, the program won't run. The code has been left in place though as an
example of the possiblities as at one time, it did run and maybe it will do so
again.
