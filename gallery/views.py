from django.shortcuts import render, get_object_or_404
from .models import Folder, Image, Tag
from .forms import ImageForm, FolderForm, TagForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# The Homepage 
def home(request):
    # If the user is logged in, show THEIR folders
    if request.user.is_authenticated:
        folders = Folder.objects.filter(user=request.user)
    else:
        # If not logged in, show nothing (or public folders if you had them)
        folders = []
    
    return render(request, 'home.html', {'folders': folders})

# The Folder Detail Page
@login_required
def folder_detail(request, folder_id):
    # added user=request.user. 
    # If the folder exists but belongs to someone else, Django returns 404 
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    
    images = folder.image_set.all()
    return render(request, 'folder_detail.html', {'folder': folder, 'images': images})

# the search thingy
@login_required
def search_results(request):
    query = request.GET.get('q')
    if query:
        
        # Add user=request.user to strictly limit results to THE currently logged in user
        images = Image.objects.filter(tags__name__icontains=query, user=request.user).distinct()
    else:
        images = []
    return render(request, 'search.html', {'images': images, 'query': query})

@login_required  # <--- This is the lock!

def upload_image(request):
    if request.method == 'POST':
        # The user hit submit! Fill the form with their data/files
        form = ImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Create the image object but don't save to DB yet
            image = form.save(commit=False)
            
            # We need to assign the current logged-in user
            image.user = request.user
            
            # Now we save it
            image.save()
            
            # We also have to save the Many-to-Many tags manually
            form.save_m2m()
            
            return redirect('home')
    else:
        # The user just arrived. Give them a blank form.
        form = ImageForm()
    
    return render(request, 'upload.html', {'form': form})

@login_required
def edit_image(request, image_id):
    # 1. Get the image
    image = get_object_or_404(Image, id=image_id)
    
    # 2. Security Check: Is this YOUR image?
    if image.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this image.")

    if request.method == 'POST':
        # 3. Process updates
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save() # Save 
            return redirect('home') # Or redirect to the folder
    else:
        # 4. Pre-fill the form with existing data
        form = ImageForm(instance=image)
    
    return render(request, 'edit_image.html', {'form': form, 'image': image})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    
    # Security Check
    if image.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this image.")
    
    if request.method == 'POST':
        image.delete()
        return redirect('home')
    
    # If they somehow get here via GET, just send them home
    return redirect('home')

# --- NEW MANAGEMENT VIEWS ---

@login_required
def manage_library(request):
    # Get only MY folders
    folders = Folder.objects.filter(user=request.user)
    # Get all tags (tags are shared)
    tags = Tag.objects.all()
    return render(request, 'manage_library.html', {'folders': folders, 'tags': tags})

# --- FOLDER LOGIC ---
@login_required
def add_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user # Auto-assign to YOU
            folder.save()
            return redirect('manage_library')
    else:
        form = FolderForm()
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add New Album'})

@login_required
def edit_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user) # Security check
    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('manage_library')
    else:
        form = FolderForm(instance=folder)
    return render(request, 'generic_form.html', {'form': form, 'title': 'Rename Album'})

@login_required
def delete_folder(request, folder_id):
    # 1. Get the folder (Securely: must belong to current user)
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    
    if request.method == 'POST':
        # 2. Deletes it (and all photos inside!!)
        folder.delete()
        # 3. Go back home
        return redirect('home')
    
    return redirect('home')

# --- TAG LOGIC ---
@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_library')
    else:
        form = TagForm()
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add New Tag'})

@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        tag.delete()
    return redirect('manage_library')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signing up
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

