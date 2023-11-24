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

urlpatterns = [
    path('', home_view, name='home'), # Change the index page
    path('landingPage/', landing_page_view, name='landing_page'), # Change the index page


    path('users/<str:username>/gardens/', garden_list_view, name='garden_list'), # Display a list of gardens to edit
    path('garden/<int:garden_id>/', garden_create_view, name='garden_create'), # Create a new garden
    path('users/<str:username>/gardens/<int:garden_id>/', garden_update_view, name='garden_update'), # Edit on on the users gardens
    path('users/<str:username>/gardens/<int:garden_id>/delete/', garden_delete_view, name='garden_delete'), # Edit one of the user posts


    path("users/", include("users.urls")),

    # Django admin site
    path('admin/', admin.site.urls),

    # Serve files in development
] 

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




