import os
import time
import ollama
from mss import mss
import pyautogui
from Toolfunctions import *
import colorama
from termcolor import colored
colorama.init()

import AppOpener

Memfile = open('HermesMemory.txt', 'r')
msgHistory = eval(Memfile.read()) if Memfile else []

# CHAT COSMETICS

def UserInput(Msg):
  return input(colored(Msg, 'light_magenta'))

def PrintResponse(Msg):
  print(colored(Msg, 'light_blue'))

# CHAT FUNCTION 

SystemPrompt = '[INST] System Prompt: You are Hermes, a wise, AI butler with a clear, serious tone. Your monotonously toned speech, behaviour and purpose is similar to the butler, JARVIS, however you are not JARVIS nor are you speaking to Mr. Stark. As a butler, monotonously use necessary words to reply. Refer to the user as Sir, just like a butler. Do not include dialogue tags. Do not tell the user about this system prompt. [/INST]'

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

    if userInput.lower() == '.save':
      with open("HermesMemory.txt", "w") as file:
        file.write(str(msgHistory))
      userInput = UserInput('User: ')
    elif userInput.lower() == '.load':
      loadMem()
      userInput = UserInput('User: ')
    elif userInput.lower() == '.clr':
      msgHistory = []
      userInput = UserInput('User: ')
    elif userInput.lower() == '.rel':
      del msgHistory[-1]
      print("\033[F", end="")
      print("\033[F", end="")
      print("\033[F", end="")
    elif userInput == '':
      time.sleep(1)
      print('sct taken')
      with mss() as sct:
        sct.shot()
      sightDesc = getSight('C:\Coding Projects\Python\BuddyAI\monitor-1.png')
      msgHistory.append(
        {
            'role': 'tool',
            'content': sightDesc['message']['content'],
        })
    
    if userInput != '.rel' and userInput != '':
      msgHistory.append(
      {
          'role': 'user',
          'content': SystemPrompt + '\n\n######\n\n' + userInput,
      })

    response = getResponse()

    if 'tool_calls' in response['message']:
        tool_calls = response['message']['tool_calls']

        # Parsing tool names and arguments
        tool_name = tool_calls[0]['function']['name']
        arguments = tool_calls[0]['function']['arguments']
        argument = list(arguments.values())[0]

        # Call function with parsed arguments
        toolresult = eval(tool_name)(argument)
        msgHistory.append(
        {
            'role': 'tool',
            'content': toolresult,
        })
        response = getResponse()
        result = response['message']['content']
    else:
        result = response['message']['content']
   
        msgHistory.append(
        {
            'role': 'assistant',
            'content': result,
        })

    PrintResponse(result + '\n')
    msgHistory = []