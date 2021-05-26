from django.contrib import admin
from .models import ModelWithImage,ModelForTwitter

# Register your models here.

admin.site.register(ModelWithImage)
admin.site.register(ModelForTwitter)
