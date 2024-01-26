from .models import ContentCategories, Comments, Content
from rest_framework import serializers


class ContentLeanSerializer(serializers.ModelSerializer):
    content_owner = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='category_name', read_only=True)

    class Meta:
        model = Content
        fields = ['comments', 'id', 'title', 'content_owner', 'post_tag', 'overview', 'created_on',
                  'views', 'updated_on', 'is_published', 'Location', 'thumbnail', 'category', 'slug']
        depth = 1

    def get_content_owner(self, obj):
        owner = obj.content_owner
        user = {'agency': owner.news_agency_name}
        return user


# ['comments', 'previous', 'next', 'id', 'title', 'content_owner', 'post_tag', 'overview', 'created_on', 'views',
#     'updated_on', 'content', 'is_published', 'Location', 'thumbnail', 'category', 'slug', 'previous_post', 'next_post']
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'


class ContentCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCategories
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    content_owner = serializers.SerializerMethodField()
    previous_post = serializers.SerializerMethodField()
    next_post = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='category_name', read_only=True)

    class Meta:
        model = Content
        fields = ['comments', 'id', 'title', 'content_owner', 'post_tag', 'overview', 'created_on', 'thumbnail_caption',
                  'views', 'updated_on', 'is_published', 'Location', 'thumbnail', 'category', 'slug', 'previous_post', 'next_post', 'content',]
        depth = 1

    def get_content_owner(self, obj):
        owner = obj.content_owner
        user = {'agency': owner.news_agency_name,
                  'email': owner.email, 'user_name': owner.user_name}
        return user

    def get_next_post(self, obj):
        next_p = obj.next_post
        next_p = {'id': next_p.id, "title": next_p.title,
                  "overview": next_p.overview[:50]}
        return next_p

    def get_previous_post(self, obj):
        previous_p = obj.previous_post
        previous_p = {'id': previous_p.id, "title": previous_p.title,
                      "overview": previous_p.overview[:50]}
        return previous_p
