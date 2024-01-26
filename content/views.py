from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Content, ContentCategories
from .serializers import ContentLeanSerializer, ContentCategoriesSerializer
from rest_framework import  status

class ListPosts(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentLeanSerializer
    
    
class ListPostCategories(ListAPIView):
    queryset = ContentCategories.objects.all()
    serializer_class = ContentCategoriesSerializer
    


