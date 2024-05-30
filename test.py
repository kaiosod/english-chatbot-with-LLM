# import chainlit as cl

# @cl.on_chat_start
# async def main():
#     elements = [
#         cl.Audio(name="example.mp3", path="example.mp3", display="inline"),
#     ]
#     await cl.Message(
#         content="Here is an audio file",
#         elements=elements,
#     ).send()

from gtts import gTTS
import os

tts = gTTS(text='Hello, how are you?', lang='en')
tts.save("output.mp3")