from django.contrib import admin
from .models import Content, Comments, ContentCategories

admin.site.register(ContentCategories)
admin.site.register(Comments)
admin.site.register(Content)
