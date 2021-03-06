# ------------------------------------------------------------------------------
# Author: Jordan K Bartos
# Date: June 9, 2019
# Description: A slackbot that generates random compliments for members in the
#              workspace.
# ------------------------------------------------------------------------------
import os
import time
import re
from slackclient import SlackClient
from Compliment import Complimentor
import random

# instantiate slackclient
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# instantiate complimentor
complimentor = Complimentor(slack_client)

#starterbot's user ID in slack: value is assigned after the bot starts up
starterbot_id = None

#constraints
RTM_READ_DELAY = 1 #seconds
COMPLIMENT_COMMAND = "compliment"
HELP_COMMAND = "help"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If it's not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mentioin (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns
        None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second roup contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Finds and executes the given command, filling in response
    response = None
    default_response = "That doesn't look like anything to me. Try *{}*.".format(HELP_COMMAND)

    # handler for the compliment command
    if command.startswith(COMPLIMENT_COMMAND):
        response = complimentor.generate_compliment(command)

    elif command.startswith(HELP_COMMAND):
        response = "`compliment` - generates a random compliment targeted at a random workspace member\n`compliment [name]` - generates a random compliment targeted at [name]\n`help` - displays this message"
    else:
        response = "Sorry, I don't understand that. Try `help` for suggestions"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel = channel,
        text = response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method 'auth.test'
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            print("command:", command)
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
