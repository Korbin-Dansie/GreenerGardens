from django.shortcuts import redirect, render

from gardens.models import Garden
from .forms import GardenForm

from django.contrib.auth.decorators import login_required

# Create your views here.
def home_view(request, *args, **kwargs):
    my_context = {
        "site_title": "Home"
    }

    if request.user.is_authenticated:
        return redirect("landing_page")

    return render(request, "home.html", my_context) # return an html template

@login_required
def landing_page_view(request, *args, **kwargs):
    current_user = request.user
    my_context = {
        "gardens": Garden.objects.filter(user=current_user),
        "site_title": "Landing Page"
    }
    return render(request, "landing.html", my_context) # return an html template

"""
    Pages to manage Gardens
"""
@login_required
def garden_create_view(request, garden_id, *args, **kwargs):
    """ Create or edit an existing portfolio item. New items have an id of 0 """
    form = GardenForm(request.POST or None)
    try:
        instance = Garden.objects.get(pk=garden_id)
    except Garden.DoesNotExist:
        instance = None

    if request.method == "POST":
        form = GardenForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.cleaned_data['user'] = request.user # Set to the current logged in user
            # save the info
            form.save()
            return redirect("home")
    else: # GET request
        form = GardenForm(instance=instance)
        form.initial['user'] = request.user.id # Set to the current logged in user

    site_title = None
    if garden_id == 0:
        site_title = "Create Garden"
    else:
        site_title = "Edit Garden"

    my_context = {
        "form": form,
        "site_title": site_title
    }
    return render(request, "users/garden_create.html", my_context) # return an html template

@login_required
def garden_update_view(request, username, garden_id, *args, **kwargs):
    """ Create or edit an existing portfolio item. New items have an id of 0 """
    form = GardenForm(request.POST or None)
    try:
        instance = Garden.objects.get(pk=garden_id)
    except Garden.DoesNotExist:
        instance = None

    # Check if logged in user made the garden
    current_user = request.user
    if(instance.user.id != current_user.id):
        return redirect("home")


    if request.method == "POST":
        form = GardenForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.cleaned_data['user'] = request.user # Set to the current logged in user
            # save the info
            form.save()
            return redirect("home")
    else: # GET request
        form = GardenForm(instance=instance)
        form.initial['user'] = request.user.id # Set to the current logged in user

    site_title = None
    if garden_id == 0:
        site_title = "Create Garden"
    else:
        site_title = "Edit Garden"

    my_context = {
        "form": form,
        "garden": instance,
        "site_title": site_title
    }
    return render(request, "users/garden_upsert.html", my_context) # return an html template

@login_required
def garden_delete_view(request, username, garden_id, *args, **kwargs):
    # Check if the user has privilege to access the post
    instance = Garden.objects.filter(user=request.user, id=garden_id)[:1] # Limit to the first post
    if(instance is None):
        redirect("users:login")
    
    form = GardenForm(instance=instance[0])
    # Update the entires
    if request.method == "POST":
        form = GardenForm(request.POST, instance=instance[0])
        if form.is_valid():
            instance[0].delete()
            return redirect("home")
    return redirect("home")

@login_required
def garden_list_view(request, username, *args, **kwargs):
    # Check if the url user is the same as the logged in user
    current_user = request.user

    if(current_user.username != username):
        return redirect("home")

    my_context = {
        "gardens": Garden.objects.filter(user=current_user),
        "site_title": "My Gardens"
    }
    return render(request, "users/garden_list.html", my_context) # return an html template
