# Dota Discord bot v2.0
# This bot has been created with the intention of improving the community of DOTA in discord servers
# Me, Jean, the creator of this robot allow the use of it for non-lucrative purposes through the GPL license
# There won't be any more updates, improvements or debugging by my part although it's allowed to fork the code by
# someone who wants to continue the work on it.


import requests
import re
from discord.ext import commands

# List which will keep the players objects
playerslist = []

# URL to use for the data output
playerinfo = "https://api.opendota.com/api/players/"


# Main object, it's used to construct the players one by one and then stored on playerlist
class Player:

    # Contructor
    def __init__(self, nome, profile_id):

        # Final URL to get the data
        response = requests.get(playerinfo + profile_id)
        # Error control routine for bad data API output
        if response.status_code != 200:
            print("Output API with problems, call the developer", response.status_code)
            return
        else:
            list = response.text.split(",")

        # Object attributes
        self.nome = nome
        self.profileid = profile_id
        self.mmr = get_mmr(list)
        self.nickname = get_nickname(list)
        self.avatar = get_avatar(list)

    # Only method to update the object's attributes
    def update(self):

        response = requests.get(playerinfo + self.profileid)
        if response.status_code > 200 or response.status_code < 200:
            print("Output API with problems, call the developer", response.status_code)
            return
        else:
            list = response.text.split(",")

        self.mmr = get_mmr(list)
        self.nickname = get_nickname(list)
        self.avatar = get_avatar(list)


# Data filtering method to extract the Player's MMR
def get_mmr(data):

    mmrdirty = []
    mmrclean = ""

    for x in data:
        mmrdirty.append(re.findall('estimate":[0-9]+', x))

    mmrdirty.sort(reverse=True)
    mmrdirty = mmrdirty[0]
    for x in mmrdirty:
        for y in x:
            if y.isdigit():
                mmrclean += y
    return int(mmrclean)

# Data filtering method to extract the Player's game nickname.
def get_nickname(data):

    dirtynick = []
    cleannick = ""

    for x in data:
        dirtynick.append(re.findall('personaname":".+', x))

    dirtynick.sort(reverse=True)
    dirtynick = dirtynick[0]
    for x in dirtynick:
        dirtynick = x

    counter = 0
    for x in dirtynick:

        if counter > 13:
            cleannick += x
        counter += 1
    return cleannick.rstrip('"')

# Data filtering method to extract the Player's game avatar.
# There isn't use now for the avatar because some channels have bug displaying it when the bot post the URL.
def get_avatar(data):

    dirtyavatar = []
    cleanavatar = ""

    for x in data:
        dirtyavatar.append(re.findall('avatarmedium":".+', x))

    dirtyavatar.sort(reverse=True)
    dirtyavatar = dirtyavatar[0]
    for x in dirtyavatar:
        dirtyavatar = x

    counter = 0
    for x in dirtyavatar:

        if counter > 14:
            cleanavatar += x
        counter += 1
    return cleanavatar.rstrip('"')
# ----------------------------------------------------------------------------------------------------------------------
# End of the object and methods definition, beginning of the bot code.
# ----------------------------------------------------------------------------------------------------------------------

# Symbol definition for the bot calls
bot = commands.Bot(command_prefix="$")

# Bot's commands decorator
@bot.command()
# Help command with whcih the user calls to get help about each other command, it's called with an argument
async def bothelp(ctx, arg):
    if arg == "create":
        await ctx.send("Adds a player to the list, it's called with two arguments, name and profileID, example: '$create Jean 51348142'")
    elif arg == "delete":
        await ctx.send("Deletes a player from the list, it's called with one argumment: profileID, example:'$delete 51348142'")
    elif arg == "leaderboard":
        await ctx.send("Returns the player's list in decrescent order of MMR, it's called without arguments, example:'$leaderboard'")
    elif arg == "mmr":
        await ctx.send("Returns the MMR of a single player, it's called with the name as argument, example: '$mmr Jean'")
    elif arg == "players":
        await ctx.send("Returns the list of registered players with name, nickname and mmr, it's called without arguments, example: '$players'")
    elif arg == "update":
        await ctx.send("Updates the data of all registered players, returns nothing, it's called without arguments, example: '$update'")
    else:
        await ctx.send("There was no arguments provided for help function, call 'commands' to know the available.")


@bot.command()
# Shows the available commands to the user
async def commands(ctx):
    await ctx.send("Available commands: '$commands', '$bothelp', '$create', '$delete', '$leaderboard', $mmr', '$players', '$update', access help to know how each one works and is called, example: '$bothelp create'")

@bot.command()
# Adds a player to the list, it's called with two arguments, name and profileID, example: '$create Jean 51348142'
async def create(ctx, name, steamid):
    for x in playerslist:
        if x.nome.lower() == name.lower():
            await ctx.send("That name is registered already, choose a different one")
            return
        if x.profileid == steamid:
            await ctx.send("That profileID is registered already.")
            return
    try:
        Player(name, steamid)
        playerslist.append(Player(name, steamid))
        await ctx.send("The player is created successfully")
    except:
        await ctx.send("There is a problem with the creation of that player, call the developer to know what happened")

@bot.command()
# Deletes a player from the list, it's called with one argument: profileID, example:'$delete 51348142'
async def delete(ctx, steamid):
    for x in playerslist:
        if x.profileid == steamid:
            playerslist.remove(x)
            del x
            await ctx.send("The player was deleted successfully")
            return
    await ctx.send("That profileID is not linked to a registered players or another argument was given")


@bot.command()
# Returns the player's list in decrescent order of MMR, it's called without arguments, example:'$leaderboard'
async def players(ctx):
    strfinal = "The registered players are: "
    for x in playerslist:
        temp = x.nome + " with nickname: " + x.nickname + " / "
        strfinal += temp
    await ctx.send(strfinal)


@bot.command()
# "Updates the data of all registered players, returns nothing, it's called without arguments, example: '$update'
async def update(ctx):
    for x in playerslist:
        try:
            x.update()
        except:
            await ctx.send("The {jogador}'s info were not updated, call the developer".format(jogador=x.nome))
    await ctx.send("The players data was updated successfully")


@bot.command()
# Returns the player's list in decrescent order of MMR, it's called without arguments, example:'$leaderboard'
async def leaderboard(ctx):
    organizada = sorted(playerslist, key=lambda x: x.mmr, reverse=True)
    counter = 1
    for x in organizada:
        await ctx.send("{contador} - {nome} / nick: {nick} / MMR: {mmr}".format(contador=counter, nome=x.nome, nick=x.nickname, mmr=x.mmr))
        counter +=1
    del organizada

@bot.command()
# Returns the MMR of a single player, it's called with the name as argument, example: '$mmr Jean'
async def mmr(ctx, nome):
   for x in playerslist:
       if x.nome.lower() == nome.lower():
           await ctx.send("{jogador}, with nickname '{nick}' has {mmr} of estimated MMR".format(jogador=x.nome, nick=x.nickname, mmr=x.mmr))
           return
   await ctx.send("That player is not registered")

# This is the location where you paste the discord key to let the bot communicate with their API.
# ----- WITHOUT THIS KEY THE BOT DOESN'T WORK -----
bot.run("XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXX")
# ----- WITHOUT THIS KEY THE BOT DOESN'T WORK -----
