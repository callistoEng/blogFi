import secrets
import string
import os
from PIL import Image
from pathlib import Path
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

class AnalyseImage:
    def __init__(self,image_name,new_size_ratio) -> None:
        self.image_name=image_name
        self.new_size_ratio=new_size_ratio

    def image_size_format(self,b, factor=1024, suffix='B'):
        # scale bytes to its proper byte format i.e 123600 ->'1.2MB'
        for unit in ['','K','M','G','T','P','E','Z']:
            if b < factor:
                return f'{b:.2f}{unit}{suffix}'
            b /= factor
        
        return f'{b:.2f}Y{suffix}'

    # def compress_image(self, image_name, new_size_ratio, quality=90, width=None, height=None, to_jpg=True):
    def compress_image(self, quality=90, width=None, height=None, to_jpg=True):
        # load image to memory
        img = Image.open(self.image_name)
        # print the original image shape
        # print('[*] Image shape: ', img.size)
        # get the original image size in bytes
        img_size = os.path.getsize(self.image_name)
        # print('[*] Size before compression: ', self.image_size_format(img_size))
        if self.new_size_ratio < 1.0:
            img = img.resize((int(img.size[0]*self.new_size_ratio), int(img.size[1]*self.new_size_ratio)), Image.ANTIALIAS)
            # print('[*] New Image shape: ', img.size)
        elif width and height:
            img = img.resize((width,height), Image.ANTIALIAS)
            # print('[*] New Image shape with H and W: ', img.size)
        return img
        # filename, ext = os.path.splitext(self.image_name)
        # if to_jpg:
        #     new_filename = f'estatecloud_{filename}_post_compressed.jpg'
        # else:
        #     new_filename= f'estatecloud_{filename}_post_compressed{ext}'
        # try:
        #     img.save(new_filename, quality=quality, optimize=True)
        # except OSError:
        #     img=img.convert('RGB')
        #     img.save(new_filename, quality=quality, optimize=True)
        # print('[*] New file saved: ', new_filename)
        # new_image_size = os.path.getsize(new_filename)
        # saving_diff = new_image_size - img_size
        # print(f'[*] File size change: {saving_diff/img_size*100:.2f}% of original ')
    
    def convert_to_webp(source):
        """Convert image to WebP.

        Args:
            source (pathlib.Path): Path to source image

        Returns:
            pathlib.Path: path to new image
        """
        destination = source.with_suffix(".webp")

        image = Image.open(source)  # Open image
        image.save(destination, format="webp")  # Convert image to webp

        return destination 
      
    def _convert_to_webp(self, f_object):
        suffix = Path(f_object._name).suffix
        if suffix == ".webp":
            return f_object._name, f_object
        
        new_file_name = str(Path(f_object._name).with_suffix('.webp'))
        image = Image.open(f_object.file)
        thumb_io = io.BytesIO()
        image.save(thumb_io, 'webp', optimize=True, quality=95)
    
        new_f_object = InMemoryUploadedFile(
            thumb_io,
            f_object.field_name,
            new_file_name,
            f_object.content_type,
            f_object.size,
            f_object.charset,
            f_object.content_type_extra
        )
        
        return new_file_name, new_f_object 

def random_string_generator(size=15, chars=string.ascii_letters + string.ascii_lowercase+string.digits):
    return ''.join(secrets.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.category_name)

    kclass = instance.__class__

    qs_exists = kclass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = '{slug}-{randstr}'.format(slug=slug, randstr=random_string_generator(size=20))
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug

def unique_listing_slug_generator(instance):
    constant_slug = slugify(instance.title)
    slug = constant_slug
    kclass = instance.__class__
    while kclass.objects.filter(slug=slug).exists():
        secrete_string = random_string_generator(size=20)
        # slug = '{slug}-{num}'.format(slug=constant_slug, num=num)
        slug = f'{slug}-{secrete_string}'
    return slug

def reference_code():
    cypher = string.ascii_uppercase + string.digits
    cypher_code = ''.join(secrets.choice(cypher) for i in range(10))
    return cypher_code


# def get_model_field_names(self):
#     fields = ModelName._meta.get_fields()
#     so = []
#     for k in fields:
#         so.append(k.name)
    
#     return so
