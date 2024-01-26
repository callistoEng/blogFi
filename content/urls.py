from django.urls import path
from .views import ListPosts, ListPostCategories, PostDetailView


urlpatterns = [
    path('', ListPosts.as_view()),
    path('detail/<str:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('categories/', ListPostCategories.as_view())
]




