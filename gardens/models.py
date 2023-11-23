from django.db import models
from django.conf import settings

# Create your models here.
class Garden(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Store the users info
    image = models.ImageField(upload_to="gardens/", blank=True, null=True) #Allow no image
    image_alt = models.CharField(max_length=255, blank=True) # Used for alt text of the image

    def __str__(self) -> str:
        return self.user.username + " - " + self.name