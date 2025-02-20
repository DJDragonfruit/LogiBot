import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sheets
from enum import Enum

# This is a list of the columns on the stock sheet
class STOCK(Enum):
    ID = 0 # Identifier number for the part
    NAME = 1 # Name of the part
    NUM = 2 # Number of the part we have (could be single or boxes)
    MIN = 3 # Minimum number of the part we want to have
    MAX = 4 # Maximum number of the part we want to have
    LINK = 5 # The link to purchase the part
    TAGS = 6 # Strings that describe the part, e.g. "bolt", "wood"




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

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")

@bot.command()
async def report(ctx):
    message = ctx.message
    message_content = message.content

    # Split into command and args
    parts = message_content.split()
    command = parts[0]
    args = parts[1:]
    await message.channel.send(f"Command: {command}, Args: {args}")

    # Decide what kind of report is needed
    for arg in args:
        match arg:
            case "stock":
                await manageStock(message.channel, command, args)
            case "tool":
                await message.channel.send("You are reporting a tool event.")

# Function to handle all arguments related to the stock sheet
async def manageStock(channel, command, args):

    await channel.send("You are reporting a stock event.")

    # Cycle through further arguments
    for arg in args:
        match arg:
            case "low":
                await channel.send("You are reporting that stock is low.")
                
    sheets.init_creds()
    await channel.send(sheets.printOut()[0])

# Run the bot with your token
bot.run(disc_token)
