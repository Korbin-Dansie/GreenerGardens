from django.shortcuts import redirect, render

from gardens.models import Garden
from .forms import GardenForm

# Create your views here.
def home_view(request, *args, **kwargs):
    my_context = {
        "site_title": "Home"
    }

    if request.user.is_authenticated:
        return redirect("landing_page")

    return render(request, "home.html", my_context) # return an html template

def landing_page_view(request, *args, **kwargs):
    current_user = request.user
    my_context = {
        "gardens": Garden.objects.filter(user=current_user),
        "site_title": "Landing Page"
    }
    return render(request, "landing.html", my_context) # return an html template

def garden_create_view(request, *args, **kwargs):
    if request.method == "POST":
        form = GardenForm(request.POST)

        if form.is_valid():
            form.cleaned_data['user'] = request.user # Set to the current logged in user
            # save the info
            form.save()
            return redirect("home")
    else: # GET request
        form = GardenForm()
        form.initial['user'] = request.user.id # Set to the current logged in user
    my_context = {
        "form": form,
        "site_title": "Create Garden"
    }
    return render(request, "users/garden_create.html", my_context) # return an html template
