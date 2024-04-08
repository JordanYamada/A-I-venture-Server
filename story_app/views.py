from django.shortcuts import render, get_object_or_404, get_list_or_404
# from rest_framework.views import APIView
from user_app.views import TokenReq
from rest_framework.response import Response
from .models import Cart, Cart_item
from item_app.models import Item
from .serializers import StorySerializer, CartItemSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
import requests
# Create your views here.

class Cart_manager(TokenReq):
    def get(self, request):
        # Get the user's cart
        cart = get_object_or_404(Cart, client=request.user)

        # Retrieve cart items associated with the cart
        cart_items = cart.cart_items.all()

        # Serialize cart items
        cart_item_serializer = CartItemSerializer(cart_items, many=True)
        
        # Calculate total price, handling None values for price and quantity
        total_price = sum((item.item.price or 0) * (item.quantity or 0) for item in cart_items)

        for cart_item in cart_items:
            cart_item.item.price = str(cart_item.item.price)

        response_data = {
            "cart_items": cart_item_serializer.data,
            "total_price": (total_price)
        }
        return Response(response_data, status=HTTP_200_OK)


    def put(self, request, cart_item_id, method):

        data = get_object_or_404(Item, id=cart_item_id)

        if data:
            cart = Cart.objects.filter(client=request.user).first()

            # If the user doesn't have a cart, create one
            if not cart:
                cart = Cart.objects.create(client=request.user)

            # Check if the item is already in the cart
            cart_item = Cart_item.objects.get(cart=cart, item=data)

            if method == 'add':
                # Increment the quantity if the item is already in the cart
                cart_item.quantity += 1
                # if cart_item.is_valid():
                cart_item.save()
            elif method == 'sub':
                cart_item.quantity -= 1
                # if cart_item.is_valid():
                if cart_item.quantity == 0:
                    cart_item.delete()
                else:
                    cart_item.save()
            response = self.get(request)
            return Response(response.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
    


    def delete(self, request, cart_item_id):

        data = get_object_or_404(Cart_item, id=cart_item_id)

        if data:
            data.delete()
            response = self.get(request)
            return Response(response.data, status=HTTP_200_OK)


        # cart_item = get_object_or_404(Item, id=cart_item_id)
        # cart = Cart.objects.filter(client=request.user).first()
        # # data = request.data.copy()
        # if method == 'add':
        #     cart_item.price += 1
        # elif method == 'sub':
        #     cart_item.price -= 1     

            
        #     else:
        #         # Increment the quantity if the item is already in the cart

        return Response(status=HTTP_400_BAD_REQUEST)
        # pass
    
