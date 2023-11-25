from django.contrib import admin

# Register your models here.
from .models import Garden
admin.site.register(Garden)

from .models import Garden_Section
admin.site.register(Garden_Section)