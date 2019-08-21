import discord
import asyncio
import time

messages = joined = 0

def read_Token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_Token()
client = discord.Client()

async def update_Stats():
    await client.wait_until_ready()
    global messages, joined
    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members joined: {joined}\n")
            messages = 0
            joined = 0
            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)




#------------------Nickname------------------------
@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("tim") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="NO STOP THAT")

@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to the server {member.mention}""")

@client.event
async def on_message(message):
    global messages
    messages += 1
    server_id = client.get_guild(612561108665892865)
    channels = ["command"]
    valid_users = ["amasu#3867"]
    
    if str(message.channel) in channels and str(message.author) in valid_users:
        if message.content.find("!hello") != -1:
            await message.channel.send("Hi")
        elif message.content == "!users":
            await message.channel.send(f"""# of Members {server_id.member_count}""")
    else:
        print(f"""User: {message.author} tried to do command {message.content}, in channel {message.channel}""")


client.loop.create_task(update_Stats())
client.run(token)
