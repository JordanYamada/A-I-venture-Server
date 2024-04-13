from django.urls import path
from .views import All_stories, A_story, Stories_by_completed
# Register the boolean converter



urlpatterns = [
    path("", All_stories.as_view(), name='all_stories'),
    path("<int:story_id>/", A_story.as_view(), name="a_story"),
    path("completed/<str:completed>/", Stories_by_completed.as_view(), name='stories_by_completed'),
]
