from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from gallery.views import home, folder_detail, search_results, upload_image, edit_image, delete_image, manage_library, add_folder, edit_folder, delete_folder, add_tag, delete_tag, register

urlpatterns = [
    path('admin/', admin.site.urls),

    # login, logout, password reset etc path
    path('accounts/', include('django.contrib.auth.urls')),

    # login path
    path('register/', register, name='register'),
    
    # empty quotes '' mean "The Homepage"
    path('', home, name='home'), 

    # path for a specific folder
    # <int:folder_id> allows the URL to change based on the folder number
    path('folder/<int:folder_id>/', folder_detail, name='folder_detail'),

    # search path
    path('search/', search_results, name='search_results'),

    # the general upload path
    path('upload/', upload_image, name='upload_image'),

    # existing upload editing path 
    path('image/<int:image_id>/edit/', edit_image, name='edit_image'),

    #existing upload deletion path
    path('image/<int:image_id>/delete/', delete_image, name='delete_image'),

    # --- LIBRARY MANAGEMENT ---
    path('manage/', manage_library, name='manage_library'),
    
    # Folder CRUD
    path('folder/add/', add_folder, name='add_folder'),
    path('folder/<int:folder_id>/edit/', edit_folder, name='edit_folder'),
    path('folder/<int:folder_id>/delete/', delete_folder, name='delete_folder'),

    # Tag Management
    path('tag/add/', add_tag, name='add_tag'),
    path('tag/<int:tag_id>/delete/', delete_tag, name='delete_tag'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)