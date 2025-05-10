import os
import time
import ollama
import AppOpener
import webbrowser
import psutil
from mss import mss
import pyautogui

from PIL import Image

from diffusers import DiffusionPipeline
import torch

# Load model locally
model_id = "stabilityai/stable-diffusion-xl-base-1.0"
pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")  # Use GPU for faster generation

def checkLoaded(AppName):
  if AppName in (i.name() for i in psutil.process_iter()):
    time.sleep(0.5)
    checkLoaded(AppName)
  else:
    time.sleep(0.5)
    return

def OpenWebsite(PageURL):
  webbrowser.open(PageURL, new=0, autoraise=True)

def SearchInternet(query):
  print('NOTICE! Search attempted on: ' + query)

def PlayMusic(SongTitle):
  print(SongTitle)
  AppOpener.open('spotify', output=False)

  checkLoaded('spotify.exe')

  pyautogui.hotkey('ctrl', 'k')
  pyautogui.write(SongTitle)
  time.sleep(2)
  pyautogui.hotkey('shift', 'enter')

  return SongTitle + ' Opened!'

def app_open(appName: str):
  
  """
  Open an application on the desktop of the human user.

    This function opens a specified application on the desktop of the user by inputting its name.

    Args:
        appName (str): Message contents. All unicode (including emojis) are supported.

    Returns:
        Optional[str]: None is always returned as this function does not produce a response.
  """
  AppOpener.open(appName.lower(), match_closest=True, output=False)
  return None

def app_close(appName):
  """
  Close an application on the desktop of the human user.

    This function closes a specified application on the desktop of the user by inputting its name.

    Args:
        appName (str): The name of the application to close.

    Returns:
        Optional[str]: None is always returned as this function does not produce a response.
  """
  AppOpener.close(appName.lower(), match_closest=True, output=False)

  return None

def app_write(content: str):
  """
  
  Press keys on the desktop of the human user.

    This function allows you to press keys on the active application on the desktop of the user by inputting a string of a combination of keys to type.

    Args:
        content (str): The string of the combination of keys to type, for example, 'w' just presses the key 'w' while a combination like 'hi this is a combination' presses all of the characters in the string in sequence.

    Returns:
        Optional[str]: None is always returned as this function does not produce a response.
  
  """

  pyautogui.write(content, interval=0.1)
  return None

# VISION FUNCTION

def screen_view():
  with mss() as sct:
    sct.shot()
  return ollama.chat(
    model='llava:13b',
    messages=[{
        'role': 'user',
        'content': 'Accurately, functionally and completely describe this entire picture very thoroughly. Segment parts of the screen for better comprehendability.',
        'image': './monitor-1.png'
      }
    ]
  )['message']['content']

def image_generate(prompt: str):
  """
  
  Generate an image and display it on the computer screen of the human user.

    This function allows you to generate an image based on a description then display it on the human user's screen for them to view.

  Args:
      prompt (str): The description of the image to generate, for example, 'Perfect, construction blueprint style, side view, rear view, Toyota Hilux'.

  Returns:
      Optional[str]: None is always returned as this function does not produce a response.
  
  """
  image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=3.5,
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator("cuda").manual_seed(0)
    ).images[0]
  
    # Save the image
  image.show()
  return None