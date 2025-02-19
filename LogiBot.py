import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the secret values
disc_token = os.getenv("DISC_TOKEN")

# Enable intents
intents = discord.Intents.default()  # Enables default intents
intents.message_content = True  # Required for reading messages

# Create bot instance with intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if message.author == bot.user:
        return

    message_content = message.content
    
    if message_content.startswith("!report"):
        parts = message_content.split()
        command = parts[0]
        args = parts[1:]
        await message.channel.send(f"Command: {command}, Args: {args}")

    for arg in args:
        match arg:
            case "stock":
                 await message.channel.send(f"You are reporting a stock event.")
            case "tool":
                await message.channel.send(f"You are reporting a tool event.")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")

# @bot.command()
# async def report(ctx):
#     await ctx.send("")

# Run the bot with your token
bot.run(disc_token)
