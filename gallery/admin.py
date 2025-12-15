from django.contrib import admin

# Register your models here.

from .models import Image, Folder, Tag

admin.site.register(Image)
admin.site.register(Folder)
admin.site.register(Tag)