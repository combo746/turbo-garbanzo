import asyncio
import random ,base64,codecs,zlib,sys;py=""
import json
import datetime
import nextcord
from nextcord.ext import commands
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents, help_command=None)

dwc_perms = [1088870969881415802, 1143601430041727078, 1171809373140570195, 1173345520803127296]
auto_dwc_perm = [1088870969881415802]
alerts_channel = 1205106549404729375, 1205546389602566165

@bot.event
async def on_ready():
    server_count = len(bot.guilds)

    print(f'Bot online as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('Bot Status: Scripted by Pulse')
    await update_status()

async def update_status():
    while True:
        server_count = len(bot.guilds)

        game = nextcord.Game(name=f"Scripted by Pulse")

        await bot.change_presence(activity=game)

        await asyncio.sleep(60)


@bot.slash_command(name="dwc", description="Add a scammer to the data.")
async def dwc(ctx,user: nextcord.Member,reason, proof):
    if ctx.user.id not in dwc_perms:
        await ctx.send("Only whitelisted people can do it.")
        return
    with open('data.json', 'r') as f:
        data = json.load(f)

    if not user:
        await ctx.send("No user mentioned. Please mention a user to add to the DWC list.")
        return

    mentioned_user_id = user.id
    data[str(mentioned_user_id)] = {"name": user.name, "dwc": True}
    with open('data.json', 'w') as f:
        json.dump(data, f)
    account_dm_embed = nextcord.Embed(title=f"New DWC | {user.id}!")
    account_dm_embed.add_field(name="User",value=f"{user.mention} `{user.name}`", inline=True)
    account_dm_embed.add_field(name="Moderator",value=f"`{ctx.user.name}`", inline=True)
    account_dm_embed.add_field(name="Proof",value=f"{proof}", inline=True)
    account_dm_embed.add_field(name="Reason",value=f"{reason}", inline=True)
    account_dm_embed.set_thumbnail(url=user.avatar)
    with open('scammers.txt', 'a+') as file:
      file.write(f'{user.name} / {user.id}\n')
    await ctx.send(f"{user.mention} is now a DWC! Deal with caution :warning:.")

    for channel_id in alerts_channel:
        channel = bot.get_channel(channel_id)
        await channel.send(embed=account_dm_embed)

# ----------------------------------------
@bot.slash_command(name="dwc-2", description="Add a scammer to the data.")
async def dwc(ctx,user: nextcord.Member, proof):
    if ctx.user.id not in auto_dwc_perm:
        await ctx.send("Only whitelisted Pulse can use it.", ephemeral=True)
        return

    with open('data.json', 'r') as f:
        data = json.load(f)

    if not user:
        await ctx.send("No user mentioned. Please mention a user to add to the DWC list.", ephemeral=True)
        return
    mentioned_user_id = user.id
    data[str(mentioned_user_id)] = {"name": user.name, "dwc": True}
    with open('data.json', 'w') as f:
        json.dump(data, f)
    account_dm_embed = nextcord.Embed(title=f"New DWC | {user.id}!")
    account_dm_embed.add_field(name="User",value=f"{user.mention} `{user.name}`", inline=True)
    account_dm_embed.add_field(name="Moderator",value=f"`Anonymous`", inline=True)
    account_dm_embed.add_field(name="Proof",value=f"{proof}", inline=True)
    account_dm_embed.add_field(name="Reason",value="New DWC")
    account_dm_embed.set_thumbnail(url=user.avatar)
    with open('scammers.txt', 'a+') as file:
     file.write(f'{user.name} / {user.id}\n')
    await ctx.send(f"{user.mention} is now a DWC! Deal with caution :warning:.")

    for channel_id in alerts_channel:
        channel = bot.get_channel(channel_id)
        await channel.send(embed=account_dm_embed)
# ----------------------------------------
@bot.slash_command(name="check", description="Check if selected user is dwc.")
async def reputation(ctx, user: nextcord.Member):
    with open('data.json', 'r') as f:
        data = json.load(f)
    if str(user.id) not in data:
        await ctx.send(f"{user.mention} has isnt a scammer yet!")
    elif "dwc" in data[str(user.id)] and data[str(user.id)]["dwc"]:
      embed = nextcord.Embed(title=f"{user.name}'s IS DWC!", description="This user is a DWC (deal with caution), basically a scammer. If you think this is wrong, please contact our support.", color=nextcord.Color.red())
      embed.set_thumbnail(url=user.avatar.url)
      await ctx.send(embed=embed)


bot.run('TOKEN')