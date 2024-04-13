from django.shortcuts import render, get_object_or_404, get_list_or_404
# from rest_framework.views import APIView
from user_app.views import TokenReq
from rest_framework.response import Response
from .models import Story
from user_app.models import Client
from progress_app.models import Progress
from progress_app.serializers import ProgressSerializer
from .serializers import StorySerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from .utils import embark_story, make_image, save_image, continue_story
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
    def get(self, request):
        
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
        
    def post(self, request):

        print("UUUUUUUSSSSSSSSSSEEEEERRRRRRRRR:",request.user)
        client = get_object_or_404(Client, email=request.user)
        print("UUUUUUUSSSSSSSSSSEEEEERRRRRRRRR:",client.id)
        data = embark_story(request)
        ai_image = make_image(data["dialogue"])   
        print(ai_image)
        new_image = save_image(ai_image)

        new_story = {
            "theme": data["theme"],
            "role": data["role"],
            "title": data["title"],
            "completed": False,
            "client": client.id,
        }

        # Create a new story instance
        story_serializer = StorySerializer(data=new_story)
        if story_serializer.is_valid():
            story = story_serializer.save()
            print(data)
            # Create a new progress instance associated with the new story

            progress_data = {
                'title': data["title"],
                'image': new_image,
                'decision': data["decision"]or None,
                'result': data["result"] or None,
                'dialogue': data["dialogue"] or None,
                'choice_one': data["choice 1"] or None,
                'danger_one': data["danger level 1"] or None,
                'choice_two': data["choice 2"] or None,
                'danger_two': data["danger level 2"] or None,
                'choice_three': data["choice 3"] or None,
                'danger_three': data["danger level 3"] or None,
                'story': story.id
            }
            progress_serializer = ProgressSerializer(data=progress_data)
            if progress_serializer.is_valid():
                progress = progress_serializer.save()

                story_data = story_serializer.data
                progress_data = progress_serializer.data

                return Response({"story":story_data, "progress":progress_data}, status=HTTP_200_OK)    
                              
            else:
                # Rollback the story creation if progress creation fails
                story.delete()
                return Response(progress_serializer.errors, status=HTTP_400_BAD_REQUEST)                    

        
        else:
            return Response(story_serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        
    

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
  


    # def delete(self, request, cart_item_id):

    #     data = get_object_or_404(Cart_item, id=cart_item_id)

    #     if data:
    #         data.delete()
    #         response = self.get(request)
    #         return Response(response.data, status=HTTP_200_OK)



    #     return Response(status=HTTP_400_BAD_REQUEST)
        pass
    
class A_story(TokenReq):
    
    def get(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        serializer = StorySerializer(story)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        serializer = StorySerializer(story)
        data = continue_story(request, serializer.data)

        if "epilogue" in data and data["epilogue"]:
            ai_image = make_image(data["epilogue"])
        else:
            ai_image = make_image(data["dialogue"])   
        print(ai_image)
        new_image = save_image(ai_image)

        print(data)
        # Create a new progress instance associated with the new story
        if "epilogue" in data and data["epilogue"]:
            progress_data = {
                'title': data["title"],
                'image': new_image,
                'decision': data["decision"]or None,
                'result': data["result"] or None,
                'epilogue': data["epilogue"] or None,
                'story': story.id
            }
            story.completed = True
            story.save()
        else:

            progress_data = {
                'title': data["title"],
                'image': new_image,
                'decision': data["decision"]or None,
                'result': data["result"] or None,
                'dialogue': data["dialogue"] or None,
                'choice_one': data["choice 1"] or None,
                'danger_one': data["danger level 1"] or None,
                'choice_two': data["choice 2"] or None,
                'danger_two': data["danger level 2"] or None,
                'choice_three': data["choice 3"] or None,
                'danger_three': data["danger level 3"] or None,
                'story': story.id
            }
        progress_serializer = ProgressSerializer(data=progress_data)
        if progress_serializer.is_valid():
            progress = progress_serializer.save()

            progress_data = progress_serializer.data

            return Response({"progress":progress_data}, status=HTTP_200_OK)

        # new_story = {
        #     "theme": data["theme"],
        #     "role": data["role"],
        #     "title": data["title"],
        #     "completed": False, 
        # }


        return Response(serializer.data, status=HTTP_200_OK)
    

    def delete(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        story.delete()
        return Response(status=HTTP_204_NO_CONTENT)

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
    

    pass


class Stories_by_completed(TokenReq):
    def get(self, request, completed):
         # Convert 'completed' parameter to boolean
        if completed.lower() in ['true', 't', '1', 'yes']:
            completed_bool = True
        elif completed.lower() in ['false', 'f', '0', 'no']:
            completed_bool = False
        else:
            return Response({'error': 'Invalid value for "completed" parameter'}, status=HTTP_400_BAD_REQUEST)
        # Get all stories based on whether they are completed or not
        stories = get_object_or_404(Story, completed=completed_bool)

        # Serialize the stories
        serializer = StorySerializer(stories, many=True)

        # Return the serialized data
        return Response(serializer.data, status=HTTP_200_OK)