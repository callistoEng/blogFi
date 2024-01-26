from .models import ContentCategories, Comments, Content
from rest_framework import serializers


class ContentLeanSerializer(serializers.ModelSerializer):
    content_owner = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field='category_name',read_only=True)
    class Meta:
        model = Content
        fields = ['comments', 'id', 'title', 'content_owner', 'post_tag', 'overview', 'created_on',
                  'views', 'updated_on', 'is_published', 'Location', 'thumbnail', 'category', 'slug']
        depth = 1

    def get_content_owner(self, obj):
        owner = obj.content_owner
        agency = {'agency': owner.news_agency_name}
        return agency


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
