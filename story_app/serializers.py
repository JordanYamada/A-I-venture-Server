from .models import Story
from rest_framework import serializers

    
class StorySerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    # cart_items = CartItemSerializer(many=True)
    class Meta:
        model = Story
        fields = "__all__"

    def get_progress(self, obj):
        return {
            'id': obj.progress.id,
            'image': obj.progress.image,
            'dialogue': obj.progress.dialogue,
            'choice_one': obj.progress.choice_one,
            'choice_two': obj.progress.choice_two,
            'choice_three': obj.progress.choice_three,
            # Add more fields as needed
        }  
    