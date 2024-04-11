import re
import json
from ai_dventure_proj.settings import env
import io
import requests
import boto3
from django.http import JsonResponse
from PIL import Image
from openai import OpenAI
import google.generativeai as genai

genai.configure(api_key=env.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

client = OpenAI(
  api_key=env.get("OPENAI_API_KEY"),
)


def embark_story(request):
  print(request.body)
  body = json.loads(request.body)
  # print("ROLE!!!!!!",body["role"])
  # print("THEME!!!!!!!!!!!!!!!!!!:", body["theme"])
  if body["theme"] == "epic adventure":
        voice = "dungeon master"
  elif body["theme"] == "space adventure":
        voice = "space captain"     

  # print("THEME!!!!:",body["theme"],"VOICE!!!!!!!!:", voice)
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"You are a {voice}."},
      {"role": "user", "content": (f'Begin a/an {body["theme"]} story about a {body["role"]}, and give me three choices to continue from. Format each choice to start as "Choice", and each choice will have a danger level shown as percentage.'+" Give me the response in a json format following this example:{title: story title, dialogue: initial story text, choice 1: choice 1 text, danger level 1: danger level pecentage, choice 2: choice 2 text, danger level 2: danger level pecentage, choice 3: choice 3 text, danger level 3: danger level percentage}")},
      # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
      # {"role": "user", "content": "Where was it played?"}
    ]
  )

  # Separate the introductory text and choices from the generated response
  story_text = response.choices[0].message.content
  print(story_text)  # This will print the entire generated story
  data = json.loads(story_text)
  print(data["choice 1"])

  # introductory_text, choices = separate_choices(story_text)

  return data
