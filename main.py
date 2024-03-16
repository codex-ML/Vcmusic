import os
import time
import asyncio
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls.types import AudioQuality
from pytgcalls.types import VideoQuality
from config import session, api_id, api_hash
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import MediaStream
from pytgcalls.types import AudioQuality
from pytgcalls.types import VideoQuality


# prints colored text
def print_line1(text):
  print("\033[38;5;226m{}\033[0m".format(text))  # yellow


def print_line2(text):
  print("\033[38;5;082m{}\033[0m".format(text))  # green


def print_line3(text):
  print("\033[38;5;208m{}\033[0m".format(text))  # light pink


# prints banner
print_line1("\n try to login\n")
time.sleep(2)
print_line2("\n login done \n")
# Create Pyrogram client
app = Client("my_account",
             api_id=api_id,
             api_hash=api_hash,
             session_string=session)

# Create PyTgCalls instance
pytg = PyTgCalls(app)


# Function to handle start command
@app.on_message(filters.command("start"))
async def handle_start_command(client, message):
  # send a reply to the user
  await message.reply("Hello, I'm a bot! How are you?")


# Function to save channel posts
@app.on_message(filters.command("save"))
async def save_channel_posts(client, message):
  # Extract arguments from the command
  command_parts = message.text.split(maxsplit=2)
  if len(command_parts) != 3:
    await message.reply_text(
        "Invalid command format. Usage: /save <file_name> <channel_id>")
    return

  file_name = command_parts[1]
  channel_id = int(command_parts[2])
