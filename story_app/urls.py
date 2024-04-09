from django.urls import path
from .views import A_story


urlpatterns = [
    path("", A_story.as_view(), name='embark'),
    # path("method/<str:method>/cart_item/<int:cart_item_id>/", Story.as_view(), name="progress"),
    # path("<int:cart_item_id>/", Story.as_view(), name='delete_item'),
]
