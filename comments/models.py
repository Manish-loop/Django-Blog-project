from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class CommentManager(models.Manager):
    def filter_by_instance(self, instance): 
        content_type = ContentType.objects.get_for_model(instance.__class__) # Used to get  content type object associated with model of instance 
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id) # It is getting superclass relating to instance in other words Comment.objects 
        return qs

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    
    objects = CommentManager() # to make sure the instance of CommentManager is available and CommentManager can override other kinds of queries 
    
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
    
    
    