from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

# Create your models here.

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None) 
        return qs
    
    def filter_by_instance(self, instance): 
        content_type = ContentType.objects.get_for_model(instance.__class__) # Used to get  content type object associated with model of instance 
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None) # It is getting superclass relating to instance in other words Comment.objects 
        return qs
    
    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class() # SomeModel is the model class object query set
            obj_qs = SomeModel.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    parent  = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    
    objects = CommentManager() # to make sure the instance of CommentManager is available and CommentManager can override other kinds of queries 
    
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']
        
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})
    
    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})
    
    def children(self):
        return Comment.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    