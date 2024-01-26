
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/',include('django_ckeditor_5.urls'), name='ck_editor_5_upload_file'), 
    path('api/v1/posts/', include('content.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
