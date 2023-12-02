from django.contrib import admin

# Register your models here.
from .models import Garden
admin.site.register(Garden)

from .models import Garden_Section
admin.site.register(Garden_Section)

from .models import Plant_Category
admin.site.register(Plant_Category)

from .models import Plant
admin.site.register(Plant)

from .models import Plant_Log
admin.site.register(Plant_Log)

from .models import Plant_Note
admin.site.register(Plant_Note)
