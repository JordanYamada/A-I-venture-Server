from django.urls import path
from .views import Story


urlpatterns = [
    path("", Story.as_view(), name='embark'),
    # path("method/<str:method>/cart_item/<int:cart_item_id>/", Story.as_view(), name="progress"),
    # path("<int:cart_item_id>/", Story.as_view(), name='delete_item'),
]
