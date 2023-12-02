"""
URL configuration for GreenerGardens project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import statistics
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from gardens.views import home_view, landing_page_view, garden_create_view, garden_update_view, garden_delete_view, garden_list_view
from gardens.views import garden_section_list_view, garden_section_create_view, garden_section_update_view, garden_section_delete_view
from gardens.views import plant_create_view, plant_update_view, plant_list_view, plant_delete_view, plant_info_view
from gardens.views import plant_log_create_view, plant_log_update_view, plant_log_delete_view
from gardens.views import plant_category_list_view, plant_category_create_view, plant_category_update_view, plant_category_delete_view
from gardens.views import note_create_view, note_update_view, note_delete_view
urlpatterns = [
    path('', home_view, name='home'), # Change the index page
    path('landingPage/', landing_page_view, name='landing_page'), # Change the index page

    # Manage garden
    path('users/<str:username>/gardens/', garden_list_view, name='garden_list'), # Display a list of gardens to edit
    path('users/<str:username>/gardens/create/', garden_create_view, name='garden_create'), # Create a new garden
    path('users/<str:username>/gardens/<int:garden_id>/', garden_update_view, name='garden_update'), # Edit the users gardens
    path('users/<str:username>/gardens/<int:garden_id>/delete/', garden_delete_view, name='garden_delete'), # Delte a garden

    # Manage garden sections
    path('users/<str:username>/gardens/<int:garden_id>/section/', garden_section_list_view, name='garden_section_list'), # Display a list of gardens sections to edit / interact with
    path('users/<str:username>/gardens/<int:garden_id>/section/create/', garden_section_create_view, name='garden_section_create'), # Create a new garden section
    path('users/<str:username>/gardens/<int:garden_id>/section/<int:section_id>/', garden_section_update_view, name='garden_section_update'), # Edit the garden section
    path('users/<str:username>/gardens/<int:garden_id>/section/<int:section_id>/delete/', garden_section_delete_view, name='garden_section_delete'), # Delete the garden section

    # Manage plants
    path('users/<str:username>/plants/', plant_list_view, name='plant_list'), # Display a list of plants to edit
    path('users/<str:username>/plants/create/', plant_create_view, name='plant_create'), # Create a new plant
    path('users/<str:username>/plants/<int:plant_id>/', plant_update_view, name='plant_update'), # Edit the plant
    path('users/<str:username>/plants/<int:plant_id>/delete/', plant_delete_view, name='plant_delete'), # Delete the plant
    path('users/<str:username>/plants/<int:plant_id>/info/', plant_info_view, name='plant_info'), # Display information about the plant, logs, notes, ect...

    # Manage plants history / logs
    path('users/<str:username>/gardens/<int:garden_id>/section/<int:section_id>/logs/create/', plant_log_create_view, name='plant_log_create'), # Create a new plant log
    path('users/<str:username>/gardens/<int:garden_id>/section/<int:section_id>/logs/<int:log_id>/', plant_log_update_view, name='plant_log_update'), # Edit the plant log
    path('users/<str:username>/gardens/<int:garden_id>/section/<int:section_id>/logs/<int:log_id>/delete/', plant_log_delete_view, name='plant_log_delete'), # Delete the plant log
    
    # Manage plants categories
    path('users/<str:username>/plants/categories/', plant_category_list_view , name='plant_category_list'), # Display a list of categories to edit
    path('users/<str:username>/plants/categories/create/', plant_category_create_view , name='plant_category_create'), # Create a new plant category
    path('users/<str:username>/plants/categories/<int:plant_category_id>/', plant_category_update_view, name='plant_category_update'), # Edit the plant category
    path('users/<str:username>/plants/categories/<int:plant_category_id>/delete/', plant_category_delete_view, name='plant_category_delete'), # Delete the plant category

    # Mange Plant Notes
    path('users/<str:username>/plants/<int:plant_id>/notes/create/', note_create_view , name='note_create'),
    path('users/<str:username>/plants/<int:plant_id>/notes/<int:note_id>/', note_update_view , name='note_update'), 
    path('users/<str:username>/plants/<int:plant_id>/notes/<int:note_id>/delete', note_delete_view , name='note_delete'), 


    # Mange login and register
    path("users/", include("users.urls")),

    # Django admin site
    path('admin/', admin.site.urls),

    # Serve files in development
] 

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




