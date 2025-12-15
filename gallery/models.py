import os
from django.db import models
from django.contrib.auth.models import User

# Imports for the thumbnail magic
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile

# 1. Tag Blueprint
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

# 2. Folder Blueprint
class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

# 3. Image Blueprint 
class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    thumbnail_file = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Relationships
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    # Overriding the save method
    def save(self, *args, **kwargs):
        # Only check if there is a file and the thumbnail is missing
        if self.image_file and not self.thumbnail_file:
            
            # 1. Open the uploaded image with Pillow
            img = PilImage.open(self.image_file)
            
            # 2. Convert to RGB (Standard for JPEGs) - handles PNG transparency issues
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 3. Resize/Scale it (Max 300x300 pixels)
            img.thumbnail((300, 300))
            
            # 4. Save this modified version to memory (not disk yet)
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            
            # 5. Create a filename (e.g., thumb_sunset.jpg)
            thumb_name = 'thumb_' + os.path.basename(self.image_file.name)
            # Ensure the extension is .jpg
            thumb_name = os.path.splitext(thumb_name)[0] + '.jpg'

            # 6. Save it to the thumbnail_file field
            self.thumbnail_file.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)

        # 7. Actually save everything to the database
        super().save(*args, **kwargs)
