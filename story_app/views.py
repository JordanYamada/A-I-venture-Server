from django.shortcuts import render, get_object_or_404, get_list_or_404
# from rest_framework.views import APIView
from user_app.views import TokenReq
from rest_framework.response import Response
# from .models import Cart, Cart_item
# from item_app.models import Item
from .serializers import StorySerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from .utils import separate_choices
import requests
import json
from ai_dventure_proj.settings import env
from openai import OpenAI
import google.generativeai as genai

genai.configure(api_key=env.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

client = OpenAI(
  api_key=env.get("OPENAI_API_KEY"),
)
# Create your views here.

class All_stories(TokenReq):
    # def get(self, request):
    #     # Get the user's cart
    #     cart = get_object_or_404(Cart, client=request.user)

    #     # Retrieve cart items associated with the cart
    #     cart_items = cart.cart_items.all()

    #     # Serialize cart items
    #     cart_item_serializer = CartItemSerializer(cart_items, many=True)
        
    #     # Calculate total price, handling None values for price and quantity
    #     total_price = sum((item.item.price or 0) * (item.quantity or 0) for item in cart_items)

    #     for cart_item in cart_items:
    #         cart_item.item.price = str(cart_item.item.price)

    #     response_data = {
    #         "cart_items": cart_item_serializer.data,
    #         "total_price": (total_price)
    #     }
    #     return Response(response_data, status=HTTP_200_OK)


    # def put(self, request, cart_item_id, method):

    #     data = get_object_or_404(Item, id=cart_item_id)

    #     if data:
    #         cart = Cart.objects.filter(client=request.user).first()

    #         # If the user doesn't have a cart, create one
    #         if not cart:
    #             cart = Cart.objects.create(client=request.user)

    #         # Check if the item is already in the cart
    #         cart_item = Cart_item.objects.get(cart=cart, item=data)

    #         if method == 'add':
    #             # Increment the quantity if the item is already in the cart
    #             cart_item.quantity += 1
    #             # if cart_item.is_valid():
    #             cart_item.save()
    #         elif method == 'sub':
    #             cart_item.quantity -= 1
    #             # if cart_item.is_valid():
    #             if cart_item.quantity == 0:
    #                 cart_item.delete()
    #             else:
    #                 cart_item.save()
    #         response = self.get(request)
    #         return Response(response.data, status=HTTP_200_OK)
    #     return Response(status=HTTP_400_BAD_REQUEST)
    


    # def delete(self, request, cart_item_id):

    #     data = get_object_or_404(Cart_item, id=cart_item_id)

    #     if data:
    #         data.delete()
    #         response = self.get(request)
    #         return Response(response.data, status=HTTP_200_OK)



    #     return Response(status=HTTP_400_BAD_REQUEST)
        pass
    
class A_story(TokenReq):
    # def get(self, request, story_id):
    #     # Get the user's cart
    #     cart = get_object_or_404(Cart, client=request.user)

    #     # Retrieve cart items associated with the cart
    #     cart_items = cart.cart_items.all()

    #     # Serialize cart items
    #     cart_item_serializer = CartItemSerializer(cart_items, many=True)
        
    #     # Calculate total price, handling None values for price and quantity
    #     total_price = sum((item.item.price or 0) * (item.quantity or 0) for item in cart_items)

    #     for cart_item in cart_items:
    #         cart_item.item.price = str(cart_item.item.price)

    #     response_data = {
    #         "cart_items": cart_item_serializer.data,
    #         "total_price": (total_price)
    #     }
    #     return Response(response_data, status=HTTP_200_OK)


    # def put(self, request, cart_item_id, method):

    #     data = get_object_or_404(Item, id=cart_item_id)

    #     if data:
    #         cart = Cart.objects.filter(client=request.user).first()

    #         # If the user doesn't have a cart, create one
    #         if not cart:
    #             cart = Cart.objects.create(client=request.user)

    #         # Check if the item is already in the cart
    #         cart_item = Cart_item.objects.get(cart=cart, item=data)

    #         if method == 'add':
    #             # Increment the quantity if the item is already in the cart
    #             cart_item.quantity += 1
    #             # if cart_item.is_valid():
    #             cart_item.save()
    #         elif method == 'sub':
    #             cart_item.quantity -= 1
    #             # if cart_item.is_valid():
    #             if cart_item.quantity == 0:
    #                 cart_item.delete()
    #             else:
    #                 cart_item.save()
    #         response = self.get(request)
    #         return Response(response.data, status=HTTP_200_OK)
    #     return Response(status=HTTP_400_BAD_REQUEST)
    


    # def delete(self, request, cart_item_id):

    #     data = get_object_or_404(Cart_item, id=cart_item_id)

    #     if data:
    #         data.delete()
    #         response = self.get(request)
    #         return Response(response.data, status=HTTP_200_OK)


    #     return Response(status=HTTP_400_BAD_REQUEST)
    def post(self, request):
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
            {"role": "user", "content": f'Begin a/an {body["theme"]} story about a {body["role"]}, and give me three choices to continue from. Format each choice to start as "Choice", and each choice will have a danger level shown as percentage. Separate each choice by a line break, but do not add any line breaks inside the choices. Example: "Choice 1...description...danger level" (all in one line).'},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            # {"role": "user", "content": "Where was it played?"}
          ]
        )

        # Separate the introductory text and choices from the generated response
        story_text = response.choices[0].message.content
        print(story_text)  # This will print the entire generated story
        introductory_text, choices = separate_choices(story_text)

        return Response({"full body":response.choices[0].message.content, "introductory_text": introductory_text, "choices": choices}, status=HTTP_200_OK)

    pass