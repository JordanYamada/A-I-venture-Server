import re
import json
import time
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

s3 = boto3.client(
    's3',
    aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY")
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





def make_image(dialogue):
    try:
        description = dialogue
        
        # Generate image using OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt=description,
            n=1,
            size="1024x1024"
        )

        print(response)

        # Extract image URL and description from response
        image_url = response.data[0].url
        # image_description = response.data[0].revised_prompt

        return image_url
    except Exception as e:
        # Error handling
        print(e)
        if hasattr(e, 'response'):
            print(e.response.status_code)
            print(e.response.data)
        else:
            print(e)

        return JsonResponse({'error': 'Unable to create an image'}, status=400)
    
  


def save_image(temp_image):
    try:
        image_url = temp_image
        print('IMAGE URL:', image_url)
        
        # Fetch the image data from the provided URL
        response = requests.get(image_url)
        image_data = io.BytesIO(response.content)
        
        # Open image using PIL
        image = Image.open(image_data)
        
        # Convert the image to JPEG format
        output = io.BytesIO()
        image.save(output, format='JPEG')
        jpeg_data = output.getvalue()
        
        # Create a unique filename
        filename = f"{int(time.time())}.jpeg"
        
        # Upload image to S3
        s3.put_object(Body=jpeg_data, Bucket='dalle-image-storage', Key=filename, ContentType='image/jpeg')
        
        # Get the URL of the uploaded image
        image_url = f"https://dalle-image-storage.s3.amazonaws.com/{filename}"
        
        return  image_url
    except Exception as e:
        print('Error proxying image:', e)
        return JsonResponse({'error': 'An error occurred while proxying the image'}, status=500)