from django import forms
from pagedown.widgets import PagedownWidget

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(widget=forms.SelectDateWidget)
    
    class Meta:
        model = Post 
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.image:  # Check if an image exists
            # Set the height and width fields manually
            instance.height_field = instance.image.height
            instance.width_field = instance.image.width
        if commit:
            instance.save()
        return instance
    

        
        
        
        