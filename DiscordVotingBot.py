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
from xml.dom.expatbuilder import parseString
import nextcord
from nextcord.ext import commands


# Path to find Credentials.txt (You'll need to change this to your own path)
CREDENTIALS_PATH = "/***/DiscordVotingBot/"

# Create bot
bot = commands.Bot(command_prefix="/")

# Set hashmap for voting topic and voting options
votingTopic = {}
votingOptions = {}
userVotes = {}
maxVotes = 3

@bot.event
async def on_ready():
    print("-" * 20)
    print("Logged in as " + bot.user.name)
    print("Bot ID:", sep = " ", end = "")
    print(bot.user.name)
    print("-" * 20)


# Allow user to use StartVote command (/startvote)
@bot.command()
async def start(ctx, *, topic = None):
    if topic == None:
        await ctx.channel.send("Please enter a topic.")
        await ctx.channel.send("Example: /start Movie Night")
        return
    # Add topic to votingTopic hashmap
    votingTopic[0] = topic
    # Show voting topic on discord
    await ctx.channel.send("Voting on: " + topic)
    # Print a message to the console
    print("Voting topic created: " + topic)
    await ctx.channel.send("Add options by using the /add <\"option\"> command")
    print("-" * 20)


@bot.command()
async def add(ctx, *, option = None):
    if option == None:
        await ctx.channel.send("Please enter an option.")
        await ctx.channel.send("Example: /add \"Inception\"")
        return
    # Add option to voting topic if there isn't already 20 options
    if len(votingOptions) < 20:
        await ctx.channel.send("Option added: " + option)
        print("Option added: " + option)
        # Add option to votingOptions hashmap
        votingOptions[len(votingOptions)] = option
        userVotes[len(userVotes)] = 0
    print("-" * 20)

@bot.command()
#show the options for the current voting topic
async def options(ctx):
    if len(votingOptions) == 0:
        await ctx.channel.send("There are no options for this voting topic.")
        return
    # Show the options and allow the user to vote for them by reacting to the message
    await ctx.channel.send("Voting options:")
    for i in range(len(votingOptions)):
        await ctx.channel.send(str(i + 1) + ": " + votingOptions[i])
    print("-" * 20)

@bot.command()
# Allow users to vote on an option
async def vote(ctx, *, option = None, maxVotes = maxVotes):
    if option == None:
        await ctx.channel.send("Please enter an option.")
        await ctx.channel.send("Example: /vote 1")
        return
    # Check if the option is a valid number
    if option.isdigit() == True:
        option = int(option)
        # Check if the option is a valid number
        if option > len(votingOptions) or option < 1:
            await ctx.channel.send("Please enter a valid option. (use /options to see options)")
            await ctx.channel.send("Example: /vote 1")
            return
    else:
        await ctx.channel.send("Please enter a valid option. (use /options to see options)")
        await ctx.channel.send("Example: /vote 1 (for the first option)")
        return
    # Check if the user has already used their max votes
    if ctx.author.name in userVotes:
        if userVotes[ctx.author.name] >= maxVotes:
            await ctx.channel.send("You have already used your max votes.")
            return
    # Add the user's vote to the userVotes hashmap
    userVotes[option - 1] = userVotes.get(option - 1, 0) + 1
    # Keep track of user's vote in userVotes hashmap
    userVotes[ctx.author.name] = userVotes.get(ctx.author.name, 0) + 1
    # Add a reaction to the message
    await ctx.message.add_reaction("\U0001F44D")
    print("User voted for option: " + str(option))
    print("-" * 20)
    # Put an embed scoreboard up using discord
    embed = discord.Embed(title = votingTopic[0], description = "", color = 0x00ff00)
    # Show all the options and their votes
    for i in range(len(votingOptions)):
        embed.add_field(name = str(i + 1) + ": " + votingOptions[i], value = str(userVotes[i]) + " votes", inline = False)
    await ctx.channel.send(embed = embed)

# Show the results of the voting
@bot.command()
async def end(ctx):
    if len(votingOptions) == 0:
        await ctx.channel.send("There are no options for this voting topic.")
        return
    # Show the results of the voting topic by using embeds
    embed = discord.Embed(title = votingTopic[0], description = "Final Results", color = 0x00ff00)
    # Show all the options and their votes
    for i in range(len(votingOptions)):
        # make sure the votes are not None
        if userVotes[i] == None:
            userVotes[i] = 0
        embed.add_field(name = str(i + 1) + ": " + votingOptions[i], value = str(userVotes[i]) + " votes", inline = False)
    await ctx.channel.send(embed = embed)
    # Reset the voting topic and options
    votingTopic = {}
    votingOptions = {}
    userVotes = {}
    # Inform guild that voting has ended.
    await ctx.channel.send("Voting topic closed.")

    



if __name__ == '__main__':
    bot.run(open(CREDENTIALS_PATH + "Credentials.txt").readline())
