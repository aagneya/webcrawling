from django.contrib import admin

# Register your models here.

from .models import Crawler

admin.site.register(Crawler)
