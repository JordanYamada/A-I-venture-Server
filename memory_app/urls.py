from django.urls import path
from .views import All_memories, A_memory




urlpatterns = [
    path("", All_memories.as_view(), name='all_memories'),
    path("<int:memory_id>/", A_memory.as_view(), name="a_memory"),
]
