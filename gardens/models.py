from django.db import models
from django.conf import settings

# Create your models here.
class Garden(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Store the users info
    
    def __str__(self) -> str:
        return self.user.username + " - " + self.name