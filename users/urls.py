from django.urls import path

from users.views import register_view
from django.contrib.auth import views as authentication_views

from .forms import UserLoginForm

app_name = "users"
urlpatterns = [
    # Get login and logout view from django
    # Default looks up for templates in registration/ so we need to change it with template name
    # Login also requires an accounts/profile/ template. Which can be chaned in setting.py with LOGIN_URL
    path('login/', authentication_views.LoginView.as_view(template_name="users/login.html", extra_context={'site_title': "Login"}, authentication_form=UserLoginForm), name='login'),
    path('logout/', authentication_views.LogoutView.as_view(template_name="users/logout.html", extra_context={'site_title': "Logout"}), name='logout'),


    # Create a custom register view
    path('register/', register_view, name='register'),

]

