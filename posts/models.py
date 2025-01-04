from django.db import models
from django.urls import reverse
import os

# Create your models here.
def upload_location(instance, filename): # where images are actually uploaded to 
    return os.path.join(str(instance.id), filename)
    # return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})
        

    class Meta:
        ordering = ["-timestamp", "-updated"]

    
    