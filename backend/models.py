from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ModelWithImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    image = models.ImageField()
    url = models.TextField()

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class ModelForTwitter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    data = models.TextField()
