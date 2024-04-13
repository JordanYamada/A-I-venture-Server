from .models import Memory
from rest_framework import serializers

    
class MemorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Memory
        fields = "__all__"