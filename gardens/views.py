from django.shortcuts import redirect, render

from gardens.models import Garden, Garden_Section, Plant, Plant_Log
from .forms import GardenForm, Garden_SectionForm, PlantForm, Plant_LogForm

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
    
    # Get the all the gardens sections
    sections = instance.sections.all()
    logs = [section.logs.all() for section in sections]
    my_context = {
        "garden": instance,
        "sections": sections,
        "logs": logs,
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
        "garden_section": instance,
        "site_title": site_title
    }
    return render(request, "users/garden_section/garden_section_create.html", my_context) # return an html template

@login_required
def garden_section_delete_view(request, username, garden_id, section_id, *args, **kwargs):
    # Check if the user has privilege to access the post
    try:
        user_garden = Garden.objects.get(user=request.user, pk=garden_id)
    except Garden.DoesNotExist:
        user_garden = None

    try:
        instance = Garden_Section.objects.filter(pk=section_id, garden=user_garden)
    except Garden_Section.DoesNotExist:
        instance = None

    if(instance is None):
        redirect("users:login")
    
    form = Garden_SectionForm(instance=instance[0])
    # Update the entires
    if request.method == "POST":
        form = Garden_SectionForm(request.POST, instance=instance[0])
        if form.is_valid():
            instance[0].delete()
            return redirect("garden_section_list", garden_id)
    return redirect("home")

"""
Manage Plants
"""
@login_required
def plant_list_view(request, username, *args, **kwargs):
    # Check if the url user is the same as the logged in user
    current_user = request.user 
    if(current_user.username != username):
        return redirect("home") 

    my_context = {
        "plants": Plant.objects.filter(user=current_user),
        "site_title": "My Gardens"
    }
    return render(request, "users/plant/plant_list.html", my_context) # return an html template

@login_required
def plant_create_view(request, username, *args, **kwargs):
    """ Create or edit an existing plant. New entries have an id of 0 """
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
def plant_update_view(request, username, plant_id, *args, **kwargs):
    """ Create or edit an existing garden item. New entries have an id of 0 """
    form = PlantForm(request.POST or None)
    try:
        instance = Plant.objects.get(pk=plant_id)
    except Plant.DoesNotExist:
        instance = None

    # Check if logged in user made the garden
    current_user = request.user
    if(instance != None):
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
    if plant_id == 0:
        site_title = "Create Garden"
    else:
        site_title = "Edit Garden"

    my_context = {
        "form": form,
        "plant": instance,
        "site_title": site_title
    }
    return render(request, "users/plant/plant_upsert.html", my_context) # return an html template

@login_required
def plant_delete_view(request, username, plant_id, *args, **kwargs):
    # Check if the user has privilege to access the plant
    instance = Plant.objects.filter(user=request.user, id=plant_id)[:1] # Limit to the first post
    if(instance is None):
        redirect("users:login")
    
    form = PlantForm(instance=instance[0])
    # Update the entires
    if request.method == "POST":
        form = PlantForm(request.POST, instance=instance[0])
        if form.is_valid():
            instance[0].delete()
            return redirect("plant_list", request.user.username)
    return redirect("home")

@login_required
def plant_info_view(request, username, plant_id, *args, **kwargs):
    try:
        instance = Plant.objects.get(pk=plant_id)
    except Plant.DoesNotExist:
        instance = None

    logs = instance.logs.all().order_by('-date', 'garden_section__garden', 'garden_section')
    # Check if logged in user made the garden
    current_user = request.user
    if(instance != None):
        if(instance.user.id != current_user.id):
            return redirect("home")
    
    # Add each year to display indvidualy
    year_list = []
    for log in logs:
        if( not log.date.year in year_list):
            year_list.append(log.date.year)

    my_context = {
        "plant": instance,
        # Order by date, garden, garden section
        "logs": logs,
        "years": year_list,
        "site_title": instance.variety + " Info"
    }

    return render(request, "users/plant/plant_info.html", my_context) # return an html template


"""
Manage Plant History / Logs
"""
@login_required
def plant_log_create_view(request, username, garden_id, section_id, *args, **kwargs):
    """ Create or edit an existing plant log. New entries have an id of 0 """
    form = Plant_LogForm(request.POST or None)

    # Check if the url user is the same as the logged in user
    try:
        section_instance = Garden_Section.objects.get(pk=section_id, garden=garden_id)
    except Garden_Section.DoesNotExist:
        section_instance = None



    # Check if logged in user made the garden section and owns the plant
    if(request.user.id != section_instance.garden.user.id):
        return redirect("home")

    if request.method == "POST":
        form = Plant_LogForm(request.POST, request.FILES)
        if form.is_valid():
            form.initial['garden_section'] = section_instance # Set to url paramater

            # Check to make sure the user owns the plant
            try:
                plant_instance = Plant.objects.get(id=form.cleaned_data['plant'].id, user=request.user.id)
            except Plant.DoesNotExist:
                plant_instance = None

            if(plant_instance is None):
                return redirect("home")
            
            # save the info
            form.save()
            return redirect('garden_section_list', request.user.username, garden_id)
    else: # GET request
        form = Plant_LogForm()
        form.initial['garden_section'] = section_id # Set to url paramater

    # Get a list of user created plants
    user_plant_list = Plant.objects.filter(user=request.user.id)
    form.fields['plant'].queryset = user_plant_list

    site_title = None
    if form.instance.pk == None:
        site_title = "Create Plant Log"
    else:
        site_title = "Edit Plant Log"

    my_context = {
        "form": form,
        "garden_id": garden_id,
        "section_id": section_id,
        "site_title": site_title
    }
    return render(request, "users/plant_log/plant_log_create.html", my_context) # return an html template

@login_required
def plant_log_update_view(request, username, garden_id, section_id, log_id, *args, **kwargs):
    """ Create or edit an existing plant log. New entries have an id of 0 """
    form = Plant_LogForm(request.POST or None)

    # Check if the url user is the same as the logged in user
    try:
        log_instance = Plant_Log.objects.get(pk=log_id, garden_section=section_id)
    except Plant_Log.DoesNotExist:
        log_instance = None

    # Check if logged in user made the garden section
    if(request.user.id != log_instance.garden_section.garden.user.id):
        return redirect("home")

    if request.method == "POST":
        form = Plant_LogForm(request.POST, request.FILES, instance=log_instance)
        if form.is_valid():
            form.initial['garden_section'] = log_instance.garden_section # Set to url paramater

            # Check to make sure the user owns the plant
            try:
                plant_instance = Plant.objects.get(id=form.cleaned_data['plant'].id, user=request.user.id)
            except Plant.DoesNotExist:
                plant_instance = None

            if(plant_instance is None):
                return redirect("home")
            
            # save the info
            form.save()
            return redirect('garden_section_list', request.user.username, garden_id)
    else: # GET request
        form = Plant_LogForm(instance=log_instance)

    # Get a list of user created plants
    user_plant_list = Plant.objects.filter(user=request.user.id)
    form.fields['plant'].queryset = user_plant_list

    site_title = None
    if form.instance.pk == None:
        site_title = "Create Plant Log"
    else:
        site_title = "Edit Plant Log"

    my_context = {
        "form": form,
        "plant_log": log_instance,
        "garden_id": garden_id,
        "section_id": section_id,
        "site_title": site_title
    }
    return render(request, "users/plant_log/plant_log_upsert.html", my_context) # return an html template

@login_required
def plant_log_delete_view(request, username, garden_id, section_id, log_id, *args, **kwargs):
    # Check if the user has privilege to access the plant
    instance = Plant_Log.objects.filter(garden_section=section_id, id=log_id)[:1] # Limit to the first post
    garden_instance = instance[0].garden_section.garden
    plant_id = instance[0].plant.id
    if(garden_instance.user.id != request.user.id):
        redirect("users:login")
    
    form = Plant_LogForm(instance=instance[0])
    # Update the entires
    if request.method == "POST":
        form = Plant_LogForm(request.POST, instance=instance[0])
        if form.is_valid():
            instance[0].delete()
            return redirect('plant_info', request.user.username, plant_id)
    return redirect("home")
