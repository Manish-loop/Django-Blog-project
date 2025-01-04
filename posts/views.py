from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm

# Create your views here.
def post_create(request):
    form = PostForm()
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Successfully Created")
            return redirect('posts:detail', id=instance.id)
        else:
            messages.error(request, "Not Successfully created")
    context = {
        "form": form
    }
    return render(request, 'posts/post_form.html', context)

def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance": instance
    }
    return render(request, 'posts/post_detail.html', context)


def post_list(request):
    queryset = Post.objects.all().order_by("-timestamp")
    context = {
            "object_list": queryset,
            "title": "List"
        }
    return render(request, 'posts/post_list.html', context)


def post_update(request, id):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(instance=instance)
    if request.method=="POST":
        form = PostForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Item Saved", extra_tags='some-tag')
            return redirect('posts:detail', id=id)
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    
    return render(request, 'posts/post_update.html', context)

def post_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")   
    return redirect('posts:list')

