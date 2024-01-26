from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings
import os
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save
from newsapp.utils import unique_slug_generator, unique_listing_slug_generator, AnalyseImage


class ContentCategories(models.Model):
    category_name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True, unique=True, db_index=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Content Categories"
        verbose_name_plural = "Content Categories"

    def __str__(self):
        return self.category_name


class Tags(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


class Comments(models.Model):
    COMMENT_STATE = (
        ('True', 'True'),
        ('False', 'False'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_comment = models.TextField(max_length=80)
    post = models.ForeignKey(
        'Content', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        get_latest_by = 'timestamp'
        verbose_name = 'Comments'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.user.email


class Content(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    content_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    post_tag = models.ForeignKey(
        Tags, on_delete=models.SET_NULL, related_name='post_tags', blank=True, null=True)
    overview = models.CharField(max_length=250, db_index=True)
    created_on = models.DateTimeField(default=now, db_index=True)
    views = models.PositiveIntegerField(blank=True, null=True, default=0)
    updated_on = models.DateTimeField(auto_now_add=True, db_index=True)
    content = CKEditor5Field(config_name='extends')
    is_published = models.BooleanField(default=False)
    Location = models.CharField(
        max_length=100, db_index=True, blank=True, null=True, default='Kenya')

    thumbnail = models.ImageField(
        upload_to='Images/contentImages/', blank=True, null=True)
    thumbnail_caption = models.CharField(
        max_length=50, blank=True, null=True)
    category = models.ForeignKey(
        ContentCategories, on_delete=models.DO_NOTHING, null=False, blank=False)
    slug = models.SlugField(max_length=250, blank=True,
                            null=False, unique=True)
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['-created_on']  # indicates decending
        verbose_name = 'Content'
        verbose_name_plural = 'Content'

    def __str__(self):
        return self.title

    # @property
    # def get_comments(self):
    #     return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comments.objects.filter(post=self).count()


class PostFiles(models.Model):
    file_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE, blank=True, null=True)
    file_name = models.CharField(
        max_length=80, db_index=True, null=True, blank=True)
    file = models.ImageField(upload_to='ckfiles/%Y/%m/%d/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        quality = 70
        to_jpg = True
        if self.file:
            image = AnalyseImage(self.file.path, 0.9)
            img = image.compress_image()
            filename, ext = os.path.splitext(self.file.path)
            img_size = os.path.getsize(self.file.path)
            if to_jpg:
                new_filename = f'{filename}.jpg'
            else:
                new_filename = f'filename{ext}'
            try:
                img.save(new_filename, quality=quality, optimize=True)
            except OSError:
                img = img.convert('RGB')
                img.save(new_filename, quality=quality, optimize=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-id']


def content_category_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def content_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_listing_slug_generator(instance)


pre_save.connect(content_category_slug_generator, sender=ContentCategories)
pre_save.connect(content_slug_generator, sender=Content)
