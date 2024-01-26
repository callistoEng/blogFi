from django.urls import path
from .views import ListPosts, ListPostCategories


urlpatterns = [
    path('', ListPosts.as_view()),
    path('categories/', ListPostCategories.as_view())
]




