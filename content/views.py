from rest_framework.views import APIView
from django.db.models import F
from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.http import Http404
from .models import Content, ContentCategories
from .serializers import ContentLeanSerializer, ContentCategoriesSerializer, ContentSerializer
from rest_framework import status


class ListPosts(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentLeanSerializer


class ListPostCategories(ListAPIView):
    queryset = ContentCategories.objects.all()
    serializer_class = ContentCategoriesSerializer


class PostDetailView(APIView):

    def get_object(self, slug):
        try:
            post = Content.objects.get(slug=slug)
            if post.views == None:
                post.views = 1
                post.save()
            else:
                post.views = F("views") + 1
                post.save()
                post.refresh_from_db()
            return post

        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        post_primitive = self.get_object(slug)
        post_serialized = ContentSerializer(post_primitive)
        return Response(data=post_serialized.data, status=status.HTTP_200_OK)


class EditPosts(APIView):

    def get_object(self, slug):
        try:
            post = Content.objects.get(slug=slug)
            return post

        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, slug, format: None):
        post_primitive = self.get_object(slug)
        post_serialized = ContentSerializer(post_primitive)
        return Response(data=post_serialized, status=status.HTTP_200_OK)
