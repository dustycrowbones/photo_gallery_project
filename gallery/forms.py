from django import forms
from .models import Image, Folder, Tag

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # We only ask for these 4 things. The user/date is automatic.
        fields = ['image_file', 'title', 'description', 'folder', 'tags']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']