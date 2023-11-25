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