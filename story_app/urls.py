from django.urls import path
from .views import All_stories, A_story


urlpatterns = [
    # path("", A_story.as_view(), name='embark'),
    path("", All_stories.as_view(), name='all_stories'),
    path("<int:id>/", A_story.as_view(), name="a_story"),
]
