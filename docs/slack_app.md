# Slack App

_configure app access inside of slack_

By the end of this step you will have named your bot and revealed the OAuth
id that Slack has assigned it. Slack requires that you first create an App and
then house a bot within it. Let's get started.

### Locate Apps

If you installed the Slack App you can open it to add an App or you can open
your browser to _https://<*YOUR WORKSPACE*>.slack.com/_. Once you are logged in
you can find _Apps_ on the lower left of the screen.

![](images/slack_app/1.png)

Select the *+* symbol to bring up apps in your browser.

### Manage Apps

![](images/slack_app/2.png)

### Build Your App

![](images/slack_app/3.png)

### Start Building

_because you can't have too many steps, right?_

![](images/slack_app/4.png)

### Create a Slack App

A popup shows up asking for your app name and development workspace.

![](images/slack_app/5.png)

### Create App

When everything is filled in, a green button in the lower right corner
of your popup turns green. Onward...

![](images/slack_app/6.png)

### Slack Bot

At this point you have created the App. The next step is to create a bot
within that app. We will start by selecting Bots as shown.

![](images/slack_app/7.png)

### Your Bot Gets a Name

The name you chose is what others in your Slack workspace will see. _You have been warned._

![](images/slack_app/8.png)

Now we need to link our new App to our current workspace to generate our 
OAuthid.

### Install App to Workspace

From the *OAuth and Permissions* menu, select the green 
*Install App to Workspace*.

![](images/slack_app/9.png)

### Give Basic Permissions to your Bot

What we are saying is that this bot is allowed to know who it's talking to.

![](images/slack_app/10.png)

### Retrieve Bot's Access Token

You need to copy the *Bot User OAuth Access Token* so you can place it into
your configuration file.

![](images/slack_app/11.png)

### Configuration File

There is a [template](conf/slack_template.ini) setup in this repository under the folder, `conf/`.

It contains a file called `slack_template.ini` which you will need to rename
to `slack.ini` and keep it in the same directory. Open your new file and
change the following lines:

```
[my-slackbot-name]
SLACK_BOT_TOKEN=xoxb-12345678910-aBCDEFGHIJKlmnoPQRSTUVWX
```

You will need to replace `xoxb-12345678910-aBCDEFGHIJKlmnoPQRSTUVWX` with the
*Bot User OAuth Access Token* you copied. Then change `my-slackbot-name` to
the name you picked for your robot.

## Congratulations

You have setup a framework in which to run your app. Now you can run the
sample app that comes with this repo to see it in action before you create
your own.