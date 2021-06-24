import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button
import time 
import json
import glob
import config

bot = commands.Bot(command_prefix='!p ')

@bot.command()
async def start(ctx, *args):
    startTime = int(time.time())
    if ctx.author.id in config.admins :

        if len(args) != 0:
            filename = 'data/'+args[0]+".csv"
        else : 
            # if the argument is empty name the file with the timestamp
            filename = 'data/'+str(time.time())+".csv"

        f = open(filename, "w")
        f.write("user,ts,status\n")
        f.close()
        
        message  = await ctx.send(
            "Cliquer ici pour confirmer votre presence",
            components = [
                Button(label = "Present", style = 3, disabled = False),
                # Button(label = "Present mais en retard", style = 4, disabled = True)
            ]
        )
        interaction = await bot.wait_for("button_click", check = lambda i: i.component.label.startswith("Present"))
        print(time.time())
        print(startTime)
        print(config.retard)
        if int(time.time()) <= (startTime + config.retard) :
            print('on time')
            await interaction.respond(content = "Presence Confirmer!")
            status = "on time"
            
        else:
            print('not on time')
            await interaction.respond(content = "Presence confirmer mais en retard!")
            status = "late"
            
        # get the data from the interaction
        interactionData = json.loads(json.dumps(interaction.raw_data))
        # get the username 
        username = interactionData['d']['member']['user']['username']
        readableTs = str(time.ctime())
        finalString = username + ',' + readableTs + ',' + status + '\n'

        # write the presence to the file
        f = open(filename, "a")
        f.write(finalString)
        f.close()
    else : 
        print('Not in list')
        message = await ctx.send('Unauthorized')
        
@bot.command(name='list')
async def _list(ctx,*args):
    if ctx.author.id in config.admins :
        if len(args) == 0 :
            dir = glob.glob('data/*')
            dirtxt = '```'
            for x in dir:
                x = x.replace('.csv', '')
                x = x.replace('data', '')
                dirtxt  += x+'\n'

            dirtxt += '```'
            await ctx.send('Please add your choice of viewing :')
            await ctx.send(dirtxt)
        else :
            file = args[0]
            f = open("data/"+args[0]+'.csv', "r")
            txt = "```"
            for x in f:
                txt += x 
            txt += '```'
            await ctx.send(txt)
    else : 
        print('Not in list')
        message = await ctx.send('Unauthorized')

# @bot.command()
# async def info(ctx,arg):
#     print('info commmand')
#     message = await ctx.send('info page')

@bot.event
async def on_ready():
    # register the button components
    DiscordComponents(bot)
    print('We have logged in as {0.user}'.format(bot))
    # https://stackoverflow.com/questions/59126137/how-to-change-discord-py-bot-activity
    await bot.change_presence(activity=discord.Game(name="Making sure you are on time"))

# launch the bot
bot.run(config.token)