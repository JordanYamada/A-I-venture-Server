from django.shortcuts import render, get_object_or_404, get_list_or_404
# from rest_framework.views import APIView
from user_app.views import TokenReq
from rest_framework.response import Response
from .models import Memory
from user_app.models import Client
from .serializers import MemorySerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
import requests
import json
from ai_dventure_proj.settings import env



# Create your views here.

class All_memories(TokenReq):

  def get(self, request):
        
        memories = Memory.objects.all()
        serializer = MemorySerializer(memories, many=True)
        return Response({"memoryData":serializer.data}, status=HTTP_200_OK)
  
  def post(self, request):
        # try:
        body = json.loads(request.body)
        client = get_object_or_404(Client, email=request.user)
        
        new_memory_data = {
            "image": body["image"],
            "dialogue": body["dialogue"],
            "title": body["title"],
            "client": client.id,
        }

        memory_serializer = MemorySerializer(data=new_memory_data)
        if memory_serializer.is_valid():
            memory_serializer.save()
            return Response(memory_serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(memory_serializer.errors, status=HTTP_400_BAD_REQUEST)

  #       except Exception as e:
  #           return Response(str(e), status=HTTP_400_BAD_REQUEST)
  # pass


class A_memory(TokenReq):

  def get(self, request, memory_id):
        memory = get_object_or_404(Memory, id=memory_id)
        serializer = MemorySerializer(memory)
        return Response(serializer.data, status=HTTP_200_OK)
  


  def delete(self, request, memory_id):
          memory = get_object_or_404(Memory, id=memory_id)
          memory.delete()
          return Response(status=HTTP_204_NO_CONTENT)    
  pass
