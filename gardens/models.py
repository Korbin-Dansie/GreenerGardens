import datetime
from django.db import models
from django.conf import settings

# Create your models here.
class Garden(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Store the users info
    image = models.ImageField(upload_to="gardens/", blank=True, null=True) #Allow no image

    def __str__(self) -> str:
        return self.user.username + " - " + self.name
    

class Garden_Section(models.Model):
    name = models.CharField(max_length=255)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name="sections") # Store the users info

    def __str__(self) -> str:
        return self.garden.name + " - " + self.name
    

class Plant_Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Store the users info

    def __str__(self) -> str:
        return self.name
    
class Plant(models.Model):
    variety = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Store the users info
    image = models.ImageField(upload_to="plants/", blank=True, null=True) #Allow no image
    category = models.ForeignKey(Plant_Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    rating = models.SmallIntegerField(default=0, blank=True)
    # seed = models.BigIntegerField(null=True, blank=True) # Check 


    def __str__(self) -> str:
        category = self.category

        if(category is not None):
            return  category.name + " - " + self.variety 
        
        return self.variety
    

class Plant_Log(models.Model):
    garden_section = models.ForeignKey(Garden_Section, on_delete=models.CASCADE, related_name="logs")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField(default=datetime.date.today)
    count = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return self.garden_section.garden.name + " - " + self.garden_section.name + " - " + self.plant.variety
    

class Plant_Note(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.DO_NOTHING, related_name="notes")
    date = models.DateField(default=datetime.date.today)
    text = models.TextField(blank=False, null=False)
