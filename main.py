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

  # Open the file in write mode
  with open(file_name, "w") as file:
    # Get the chat history of the channel
    async for msg in client.iter_history(channel_id):
      # Save the message id to the file
      file.write(f"{msg.message_id}\n")

  # Send the file to the user who sent the command
  await client.send_document(message.chat.id, file_name)



@app.on_message(filters.command("join"))
async def join(client, message):
         commands = message.text.split(maxsplit=1)
         if  len(commands) != 2:
           await message.reply_text("invalid command")
         print(commands)
         chat_id = commands[1]
         await pytg.join_group_call(chat_id,MediaStream("lol.mp3",AudioQuality.HIGH,
          video_flags=MediaStream.IGNORE),)




@app.on_message(filters.command('Lplay'))
async def play_handler(_, message):
  replied_message = message.reply_to_message

  if not replied_message or not replied_message.audio:
    await message.reply_text("Reply to an audio message to play it.")
    return

  audio_file_path = f"{replied_message.audio.file_id}.ogg"

  # Download the audio using Pyrogram's download_media
  audio_file = await app.download_media(replied_message.audio)

  # Play the downloaded audio using ffplay
  await pytg.join_group_call(
      message.chat.id,
      MediaStream(
          audio_file,
          AudioQuality.HIGH,
          video_flags=MediaStream.IGNORE,
          # VideoQuality.HD_720P,
      ),
  )

  # # Wait for the playback to finish
  # play_process.wait()

  # # Clean up the downloaded audio file
  # subprocess.run(["rm", audio_file])


@app.on_message(filters.regex('volume (\d+)'))
async def vol(client, message):
    volume_level = int(message.matches[0].group(1))
    await pytg.change_volume_call(
        message.chat.id,
        volume_level
    )


@app.on_message(filters.regex('.pause'))
async def pause_handler(_: Client, message: Message):
  await message.reply_text(text="Userbot  paused song")
  await pytg.pause_stream(message.chat.id, )


@app.on_message(filters.regex('.stop'))
async def stop_handler(_: Client, message: Message):
  await message.reply_text(text="Userbot  stopped song.")
  await pytg.leave_group_call(message.chat.id, )


@app.on_message(filters.regex('.resume'))
async def resume_handler(_: Client, message: Message):
  await message.reply_text(text="Userbot  resume song")
  await pytg.resume_stream(message.chat.id, )


pytg.start()

idle()
