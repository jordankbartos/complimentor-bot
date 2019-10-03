# ComplimentorBot
A slackbot that generates random compliments for friends and colleagues

#### To get started with this slackbot, follow these steps
1. Clone this repository or download and extract the files to a folder on your system
2. Install virtualenv on your system. `sudo apt install virtualenv`
3. Create a virtual environment in which to run this slack bot. `virtualenv Complimentor`
4. Install slackclient in the virtual environment. `pip install slackclient`
5. At https://api.slack.com/apps/new, create a Slack App, and copy its Bot User OAuth Access Token
6. Save the token as an environment variable in your virtual environment. `export SLACK_BOT_TOKEN='[your bot user access token]'`
7. Begin the slack bot with the command `python ComplimentorBot.py`
 
#### ComplimentorBot Operation
* The bot will load a basic library from the adjectives.txt, adverbs.txt, and nouns.txt files in the system. It will load the names of all the users in the slack workspace upon starting up.
###### ComplimentorBot Commands
* `@ComplimentorBot compliment` - generates a random compliment targeted at a random person in the workspace.<br>
* `@ComplimentorBot compliment @[name]` - generates a random compliment targeted at [name]. If [name] is the name or handle of someone in your workspace, ComplimentorBot will compliment them with an @ mention.

#### Upcoming Features
* the ability to add words to the ComplimentorBot's library by the slack workspace's users via a bot command,
* transitioning the vocabulary storage away from text-based .txt files and into a proper database such as postgreSQL,
* and moving from @ commands to / commands which requires a major overhaul of the bot's code-base.


#### Known Issues
* If the connection is interuppted for a moment, Complimentor bot does not attempt to reconnect automatically. Instead, an exception is thrown and the program terminates.
