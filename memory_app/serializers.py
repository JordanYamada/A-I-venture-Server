from .models import Memory
from rest_framework import serializers

    
class ProgressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Memory
        fields = "__all__"