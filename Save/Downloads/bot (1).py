import discord
from discord.ext import commands
import requests
from datetime import datetime
import random
from discord.ext.commands import cooldown, BucketType
import pytz


TOKEN = 'token'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name="gen")
@cooldown(1, 10, BucketType.user)
async def gen(ctx):
    try:
        with open('stock.txt', 'r+') as file:
            lines = file.readlines()
            if lines:
                content = lines[0].strip()
                username, password = content.split(':')

                payload = {
                    "usernames": [
                        username
                    ],
                    "excludeBannedUsers": True
                }

                response = requests.post(
                    'https://users.roblox.com/v1/usernames/users',
                    headers={
                        'accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    json=payload
                )

                response_data = response.json()
                user_id = response_data['data'][0]['id']

                creation_response = requests.get(
                    f'https://users.roblox.com/v1/users/{user_id}')
                creation_data = creation_response.json()
                created_date = creation_data['created'][:10]

                last_online_response = requests.get(
                    f'https://rblx.trade/api/v2/users/{user_id}/last-online')
                last_online_data = last_online_response.json()
                last_online_date = last_online_data['lastOnline'][:10]

                avatar_response = requests.get(
                    f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=720x720&format=Png&isCircular=false")
                if avatar_response.status_code == 200:
                    avatar_data = avatar_response.json()
                    image_url = avatar_data['data'][0]['imageUrl']
                else:
                    image_url = None

                embed = discord.Embed(title=f"Account generated | {username}",
                                      url=f"https://www.roblox.com/users/{user_id}/profile")

                embed.add_field(name="Username:",
                                value=f"```{username}```", inline=True)
                embed.add_field(name="Password:",
                                value=f"```{password}```", inline=True)
                embed.add_field(
                    name="Combo:", value=f"```{content}```", inline=False)
                embed.add_field(name="User ID:", value=user_id, inline=True)
                embed.add_field(
                    name="Last Online:", value=f"<t:{int(datetime.fromisoformat(last_online_date).timestamp())}:R>", inline=True)
                embed.add_field(
                    name="Created:", value=f"<t:{int(datetime.fromisoformat(created_date).timestamp())}:R>", inline=True)

                if image_url:
                    embed.set_thumbnail(url=image_url)

                embed.set_footer(
                    text="⚠️ If you intend to keep this account, then change the password!")

                await ctx.send(embed=discord.Embed(title="Account generated",
                                                   description="Check your DMs",
                                                   timestamp=datetime.now()))
                await ctx.author.send(embed=embed)

                file.seek(0)
                file.truncate()
                file.writelines(lines[1:])
            else:
                await ctx.send('Stock file is empty.')

    except FileNotFoundError:
        await ctx.send('Stock file not found.')
    except Exception as e:
        await ctx.send(f'Error: {e}')


@gen.error
async def gen_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You are on cooldown. Please wait {round(error.retry_after)} seconds before using this command again.')


bot.run(TOKEN)
