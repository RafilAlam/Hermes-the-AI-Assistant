import ollama
from mss import mss
import pyautogui

from LettaTools.client import *
import colorama
from termcolor import colored
colorama.init()

# TTS ENGINE
from RealtimeTTS import TextToAudioStream, CoquiEngine
if __name__ == '__main__':
  engine = CoquiEngine(model_name="tts_models/multilingual/multi-dataset/xtts_v2", specific_model='v2.0.3', voices_path='Voice Samples', temperature=0.00000001, speed=1.2) # replace with your TTS engine
  stream = TextToAudioStream(engine)

  def VoiceMsg(msg):
      stream.feed(msg)
      stream.play()
  # CHAT COSMETICS

  def UserInput(Msg):
    return input(colored(Msg, 'light_magenta'))

  def PrintThoughts(Msg):
    print(colored(Msg, 'white', attrs=['bold', 'dark']))

  def PrintResponse(Msg):
    print(colored(Msg, 'light_blue'))

  # CHAT FUNCTION 

  def loadMem():
    with open('HermesMemory.txt', 'r') as file:
      global msgHistory
      msgHistory = eval(file.read())

  def getResponse():
    return ollama.chat(
      model='mistral-nemo:latest',
      options={"temperature":1},
      messages=msgHistory,

      tools=[{
        'type': 'function',
        'function': {
          'name': 'OpenApp',
          'description': 'Open an application that may be of use to the user.',
          'parameters': {
            'type': 'object',
            'properties': {
              'appName': {
                'type': 'array',
                'description': 'name of the application you would like to open',
              },
            },
            'required': ['appName'],
              },
            },
          },
          {
        'type': 'function',
        'function': {
          'name': 'CloseApp',
          'description': 'Close an application for the user when requested or when they are done with it.',
          'parameters': {
            'type': 'object',
            'properties': {
              'appName': {
                'type': 'array',
                'description': 'name of the application you would like to close',
              },
            },
            'required': ['appName'],
              },
            },
          },
          {
        'type': 'function',
        'function': {
          'name': 'PlayMusic',
          'description': 'Play music from spotify for the user.',
          'parameters': {
            'type': 'object',
            'properties': {
              'SongTitle': {
                'type': 'string',
                'description': 'name of the song you would like to play',
              },
            },
            'required': ['SongTitle'],
              },
            },
          },
          {
        'type': 'function',
        'function': {
          'name': 'OpenWebsite',
          'description': 'Open a website for the user.',
          'parameters': {
            'type': 'object',
            'properties': {
              'PageURL': {
                'type': 'string',
                'description': 'URL of the website you would like to visit',
              },
            },
            'required': ['PageURL'],
              },
            },
          },
          {
        'type': 'function',
        'function': {
          'name': 'SearchInternet',
          'description': 'Access more information from the internet to use in replying to the user.',
          'parameters': {
            'type': 'object',
            'properties': {
              'query': {
                'type': 'string',
                'description': 'Your query',
              },
            },
            'required': ['query'],
              },
            },
          },
        ]
      )

  while True:
      userInput = UserInput('\nUser: ')

      InternalMonologue, Response = UserChat(userInput)
      if type(InternalMonologue) == str:
        PrintThoughts('\n💭 Thoughts: ' + InternalMonologue)
      if type(Response) == str:
        PrintResponse('🤖 Assistant: ' + Response + '\n')
        VoiceMsg(Response)