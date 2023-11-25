from django.shortcuts import redirect, render

from gardens.models import Garden, Garden_Section
from .forms import GardenForm, Garden_SectionForm, PlantForm

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
def garden_create_view(request, username, *args, **kwargs):
    """ Create or edit an existing garden. New entries have an id of 0 """
    form = GardenForm(request.POST or None)

    if request.method == "POST":
        form = GardenForm(request.POST, request.FILES)

        if form.is_valid():
            form.cleaned_data['user'] = request.user # Set to the current logged in user
            # save the info
            form.save()
            return redirect("home")
    else: # GET request
        form = GardenForm()
        form.initial['user'] = request.user.id # Set to the current logged in user

    site_title = None
    if form.instance.pk == None:
        site_title = "Create Garden"
    else:
        site_title = "Edit Garden"

    my_context = {
        "form": form,
        "site_title": site_title
    }
    return render(request, "users/garden/garden_create.html", my_context) # return an html template

@login_required
def garden_update_view(request, username, garden_id, *args, **kwargs):
    """ Create or edit an existing garden item. New entries have an id of 0 """
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
    return render(request, "users/garden/garden_upsert.html", my_context) # return an html template

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
    return render(request, "users/garden/garden_list.html", my_context) # return an html template


"""
    Pages to manage Gardens Sections
"""
@login_required
def garden_section_list_view(request, username, garden_id, *args, **kwargs):
    # Check if the url user is the same as the logged in user
    try:
        instance = Garden.objects.get(pk=garden_id)
    except Garden.DoesNotExist:
        instance = None

    # Check if logged in user made the garden
    current_user = request.user
    if(current_user.id != instance.user.id):
        return redirect("home")

    my_context = {
        "garden": instance,
        "sections": instance.sections.all(),
        "site_title": "My Gardens - " + instance.name,
    }
    return render(request, "users/garden_section/garden_section_list.html", my_context) # return an html template

@login_required
def garden_section_create_view(request, username, garden_id, *args, **kwargs):
    """ Create or edit an existing garden section. New entries have an id of 0 """
    form = Garden_SectionForm(request.POST or None)
    
    try:
        user_garden = Garden.objects.get(user=request.user, pk=garden_id)
    except Garden.DoesNotExist:
        user_garden = None


    if request.method == "POST":
        form = Garden_SectionForm(request.POST, request.FILES)

        if form.is_valid():
            # Set form data equal to url data to make sure its not changed
            form.cleaned_data['garden'] = form.cleaned_data['garden']

            # Check if forms garden id is in users gardens that they made
            if(user_garden == None):
                return redirect("home")

            # save the info
            form.save()
            return redirect("garden_section_list", username, garden_id)
    else: # GET request
        form = Garden_SectionForm()
        form.initial['garden'] = garden_id # Set to the url garden

    site_title = None
    if form.instance.pk == None:
        site_title = "Create Garden Section"
    else:
        site_title = "Edit Garden Section"

    my_context = {
        "form": form,
        "garden": user_garden, # Get first garden
        "site_title": site_title
    }
    return render(request, "users/garden_section/garden_section_create.html", my_context) # return an html template

@login_required
def garden_section_update_view(request, username, garden_id, section_id, *args, **kwargs):
    """ Create or edit an existing garden section. New entries have an id of 0 """
    form = Garden_SectionForm(request.POST or None)
    
    try:
        user_garden = Garden.objects.get(user=request.user, pk=garden_id)
    except Garden.DoesNotExist:
        user_garden = None

    try:
        instance = Garden_Section.objects.get(pk=section_id)
    except Garden.DoesNotExist:
        instance = None


    if request.method == "POST":
        form = Garden_SectionForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            # Set form data equal to url data to make sure its not changed
            form.cleaned_data['garden'] = form.cleaned_data['garden']

            # Check if forms garden id is in users gardens that they made
            if(user_garden == None):
                return redirect("home")

            # save the info
            form.save()
            return redirect("garden_section_list", username, garden_id)
    else: # GET request
        form = Garden_SectionForm(instance=instance)
        form.initial['garden'] = garden_id # Set to the url garden

    site_title = None
    if form.instance.pk == None:
        site_title = "Create Garden Section"
    else:
        site_title = "Edit Garden Section"

    my_context = {
        "form": form,
        "garden": user_garden, # Get first garden
        "site_title": site_title
    }
    return render(request, "users/garden_section/garden_section_create.html", my_context) # return an html template


"""
Manage Plants
"""
@login_required
def plant_create_view(request, username, *args, **kwargs):
    """ Create or edit an existing garden. New entries have an id of 0 """
    form = PlantForm(request.POST or None)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)

        if form.is_valid():
            form.cleaned_data['user'] = request.user # Set to the current logged in user
            # save the info
            form.save()
            return redirect("home")
    else: # GET request
        form = PlantForm()
        form.initial['user'] = request.user.id # Set to the current logged in user

    site_title = None
    if form.instance.pk == None:
        site_title = "Create Plant"
    else:
        site_title = "Edit Plant"

    my_context = {
        "form": form,
        "site_title": site_title
    }
    return render(request, "users/plant/plant_create.html", my_context) # return an html template

@login_required
def plant_update_view(request, username, garden_id, *args, **kwargs):
    """ Create or edit an existing garden item. New entries have an id of 0 """
    form = PlantForm(request.POST or None)
    try:
        instance = Garden.objects.get(pk=garden_id)
    except Garden.DoesNotExist:
        instance = None

    # Check if logged in user made the garden
    current_user = request.user
    if(instance.user.id != current_user.id):
        return redirect("home")


    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.cleaned_data['user'] = request.user # Set to the current logged in user
            # save the info
            form.save()
            return redirect("home")
    else: # GET request
        form = PlantForm(instance=instance)
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
    return render(request, "users/garden/garden_upsert.html", my_context) # return an html template
