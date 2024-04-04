from .models import Story
from rest_framework import serializers

  

# class CartItemSerializer(serializers.ModelSerializer):
#     item = serializers.SerializerMethodField()

#     class Meta:
#         model = Cart_item
#         fields = [
#             "id",
#             "item",
#             "quantity",
#         ]

#     def get_item(self, obj):
#         # Assuming 'item' is a related field in your CartItem model,
#         # you can define the logic to retrieve the item data here.
#         return {
#             'id': obj.item.id,
#             'category': obj.item.category,
#             'name': obj.item.name,
#             'price': obj.item.price,
#             # Add more fields as needed
#         }

    
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
    