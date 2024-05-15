import re
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Story
import json
import time
import io
import requests
import boto3
from django.http import JsonResponse
from PIL import Image
from openai import OpenAI
import os




client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)


def embark_story(request):
  print(request.body)
  body = json.loads(request.body)

  if body["theme"] == "epic adventure":
        voice = "dungeon master"
  elif body["theme"] == "space adventure":
        voice = "space captain"     

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"You are a {voice}."},
      {"role": "user", "content": (f'Begin a/an {body["theme"]} story about a {body["role"]}, and give me three choices to continue from. Format each choice to start as "Choice", and each choice will have a danger level shown as percentage. Do not offer any choices that have been previously chosen, but replace it with a new choice, so that there will always be three choices offered. keep count of how many choices I have chosen. If 4 choices have been chosen by me, conclude the story with an epilogue and do not offer any more choices.'+' until the conclusion, always give me the response in a JSON object following this example:{"title": story title, "dialogue": if no response from a choice: initial story text, else: response from chosen choice, "choice 1": random story choice 1, "danger level 1": danger level percentage, "choice 2": random story choice 2, "danger level 2": danger level percentage, "choice 3": random story choice 3, "danger level 3": danger level percentage, "choices made": number of choices chosen so far }. When choices made is 4, conclude the story with an epilogue, give me the response in a json format following this example:{"title": story title, "epilogue":  epilogue}. MAKE SURE THE RESPONSE is Always a JSON object.') },
    ]
  )

  # Separate the introductory text and choices from the generated response
  story_text = response.choices[0].message.content
  print("SSSTTTOOORRRYYY" , type(story_text),story_text)  # This will print the entire generated story


  decision = f'Begin a/an {body["theme"]} about a {body["role"]}, and give me three choices to continue from. Format each choice to start as "Choice", and each choice will have a danger level shown as percentage. Do not offer any choices that have been previously chosen, but replace it with a new choice, so that there will always be three choices offered. keep count of how many choices I have chosen. If 4 choices have been chosen by me, on the next choice, must conclude the story with an epilogue and do not offer any more choices.'+' until the conclusion, always give me the response in a JSON object following this example:{"title": story title, "dialogue": if no response from a choice: initial story text, else: response from chosen choice, "choice 1": random story choice 1, "danger level 1": danger level percentage, "choice 2": random story choice 2, "danger level 2": danger level percentage, "choice 3": random story choice 3, "danger level 3": danger level percentage, "choices made": number of choices chosen so far }. Keep track of "choices made, and hen "choices made" is 4, conclude the story with an epilogue, give me the response in a json format following this example:{"title": story title, "epilogue": epilogue}. MAKE SURE THE RESPONSE is Always a JSON object.'


  data = json.loads(story_text)
  data["theme"]= body["theme"]
  data["role"] = body["role"]
  data["decision"] = decision
  data["result"] = story_text


  return data




def continue_conversation(*args):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=list(args)
    )
    return response.choices[0].message.content




def continue_story(request, story):
    
    data = json.loads(request.body)
    choice = data["choice"]
    if story["theme"] == "epic adventure":
          voice = "dungeon master"
    elif story["theme"] == "space adventure":
          voice = "space captain"
      

    # Example usage
    past_messages = [
        {"role": "system", "content": f"You are a {voice}."}
    ]

    for moment in story["progress"]:
        past_messages.append({"role": "user", "content": moment["decision"]})
        past_messages.append({"role": "assistant", "content": moment["result"]})

    past_messages.append({"role": "user", "content": choice})

    # Continue the conversation
    story_text = continue_conversation(*past_messages)

    data = json.loads(story_text)


    
    data["theme"] = story["theme"]
    data["role"] = story["role"]
    data["decision"] = choice
    data["result"] = story_text
    print("Assistant:", data)

    return data





def make_image(dialogue):
    try:
        description = dialogue
        
        # Generate image using OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"{description} Do Not Add Text to the Image",
            n=1,
            size="1024x1024"
        )

        print(response)

        # Extract image URL and description from response
        image_url = response.data[0].url

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