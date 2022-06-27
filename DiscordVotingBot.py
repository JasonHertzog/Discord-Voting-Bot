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

# Things the bot must at least be able to do
# Add options to the menu
# Admins can delete options from the menu
# Admins can clear the menu
# Admins can close the poll

# Importing the necessary modules
import nextcord as discord
from nextcord.ext import commands


# Path to find Credentials.txt (You'll need to change this to your own path)
CREDENTIALS_PATH = "/PUT_YOUR_PATH_HERE_DONT_IGNORE_THIS/"

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
@bot.slash_command("start", "Start a vote by typing /start <voting topic>")
async def start(ctx, *, topic = None):
    if topic == None:
        await ctx.send("Please enter a topic.")
        await ctx.send("Example: /start Movie Night")
        return
    # Make sure that there isn't already an active vote.
    if len(votingTopic) != 0:
        await ctx.send("There is already a voting topic.")
        return
    # Add topic to votingTopic hashmap
    votingTopic[0] = topic
    # Show voting topic on discord
    await ctx.channel.send("Voting on: " + topic)
    # Print a message to the console
    print("Voting topic created: " + topic)
    await ctx.send("Add options by using the /add <\"option\"> command")
    print("-" * 20)


@bot.slash_command('add', "Add an option to the voting topic")
async def add(ctx, *, option = None):
    if option == None:
        await ctx.send("Please enter an option.")
        await ctx.send("Example: /add \"Inception\"")
        return
    # Add option to voting topic if there isn't already 20 options
    if len(votingOptions) < 20:
        #reply to the user to let them know the option was dded.
        await ctx.send("Option added: " + option)
        print("Option added: " + option)
        # Add option to votingOptions hashmap
        votingOptions[len(votingOptions)] = option
        userVotes[len(userVotes)] = 0
    print("-" * 20)

@bot.slash_command("choices", "Show the choices for the current voting topic")
#show the options for the current voting topic
async def options(ctx):
    if len(votingOptions) == 0:
        await ctx.send("There are no options for this voting topic.")
        return
    # Use embed to show the options
    embed = discord.Embed(title = "Voting Options", description = "", color = 0x00ff00)
    for i in range(len(votingOptions)):
        embed.add_field(name = str(i + 1) + ". " + votingOptions[i], value = "/vote " + str(i + 1), inline = False)
    await ctx.channel.send(embed = embed)
    # Show the options and allow the user to vote for them by reacting to the message
    await ctx.send("Voting options:")
    for i in range(len(votingOptions)):
        await ctx.send(str(i + 1) + ": " + votingOptions[i])
    print("-" * 20)

@bot.slash_command("vote", "Cast a vote for an option")
# Allow users to vote on an option
async def vote(ctx, *, options = None):
    if options == None:
        await ctx.send("Please enter an option.")
        await ctx.send("Example: /vote 1")
        return
    # Check if the option is a valid number
    if options.isdigit() == True:
        options = int(options)
        # Check if the option is a valid number
        if options > len(votingOptions) or options < 1:
            await ctx.send("Please enter a valid option. (use /options to see options)")
            await ctx.send("Example: /vote 1")
            return
    else:
        await ctx.send("Please enter a valid option. (use /options to see options)")
        await ctx.send("Example: /vote 1 (for the first option)")
        return
    # Check if the user has already used their max votes
    if ctx.user in userVotes:
        if userVotes[ctx.user] >= maxVotes:
            await ctx.send("You have already used your max votes.")
            return
    # Add the user's vote to the userVotes hashmap
    userVotes[options - 1] = userVotes.get(options - 1, 0) + 1
    # Keep track of user's vote in userVotes hashmap
    userVotes[ctx.user] = userVotes.get(ctx.user, 0) + 1
    # Add a reaction to the message
    print("User voted for option: " + str(options))
    print("-" * 20)
    # Put an embed scoreboard up using discord
    embed = discord.Embed(title = votingTopic[0], description = "", color = 0x00ff00)
    # Show all the options and their votes
    for i in range(len(votingOptions)):
        embed.add_field(name = str(i + 1) + ": " + votingOptions[i], value = str(userVotes[i]) + " votes", inline = False)
    await ctx.channel.send(embed = embed)

# Show the results of the voting
@bot.slash_command("end", "End the vote.")
async def end(ctx):
    if len(votingOptions) == 0:
        await ctx.send("There are no options for this voting topic.")
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
    resetHashmaps()
    # Inform guild that voting has ended.
    await ctx.send("Voting topic closed.")

    # Easter egg command: Who is most skilled?
@bot.slash_command("mostskilled", "Show the most skilled user to have ever existed.")
async def mostskilled(ctx):
    await ctx.send("The most skilled user to have ever existed is: Skilled Apple#5994")
    await ctx.channel.send("If I do anything stupid, message him and he'll tell you to fix it yourself.")

    
def resetHashmaps():
    votingOptions.clear()
    votingTopic.clear()
    userVotes.clear()


if __name__ == '__main__':
    bot.run(open(CREDENTIALS_PATH + "Credentials.txt").readline())
