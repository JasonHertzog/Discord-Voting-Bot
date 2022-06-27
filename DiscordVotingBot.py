# A bot that allows users to vote for various things through Discord.

# How it works:
# 1. The bot connects to Discord and logs in.
# 2. The bot listens for commands from users.  
# 3. If the bot sees a command it knows, it executes the command.

# Voting commands:
# /startVote <voting topic> <voting option 1...n, max of 20> (Based on array that can be added to by !addoption)
# /addOption <option to add> (Adds an option to the voting topic) (Max of 20 options)
# /maxVotes <number of votes> (Sets the maximum number of votes per user) (Max of 3 by default)
# /endVote (Ends the voting topic)
# /vote <option number> (Votes for an option)
# /results (Shows the results of the voting topic) (This is used automatically when !endvote is used)
# /help (Shows the commands with an explanation)
# All commands can be used by interacting with reactions on the voting topic.

# Importing the necessary modules
import nextcord as discord
from nextcord.ext import commands

# Path to find Credentials.txt (You'll need to change this to your own path)
CREDENTIALS_PATH = "YOUR_DIRECTORY/DiscordVotingBot/"

# Create bot
bot = commands.Bot(command_prefix="/")

@bot.event
async def on_ready():
    print("-" * 20)
    print("Logged in as " + bot.user.name)
    print("Bot ID:", sep = " ", end = "")
    print(bot.user.id)
    print("-" * 20)




if __name__ == '__main__':
    bot.run(open(CREDENTIALS_PATH + "Credentials.txt").readline())