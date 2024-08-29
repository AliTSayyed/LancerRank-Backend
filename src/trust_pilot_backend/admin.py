from django.contrib import admin

from .models import Reviews, Freelancers, Users

# give admin site access to the models created in models.py. 
# Must create a superuser to login to the admin site. 
admin.site.register(Reviews)
admin.site.register(Freelancers)
admin.site.register(Users)