from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm

# Create your views here.
def post_create(request):
    form = PostForm()
    if request.method=="POST":
        form = PostForm(request.POST, request.FILES)
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

def post_detail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    context = {
        "title": instance.title,
        "instance": instance
    }
    return render(request, 'posts/post_detail.html', context)


def post_list(request):
    queryset_list = Post.objects.all() 
    paginator = Paginator(queryset_list, 25) 

    page_number = request.GET.get("page")
    queryset = paginator.get_page(page_number)
    context = {
            "object_list": queryset,
            "title": "List"
        }
    return render(request, 'posts/post_list.html', context)


def post_update(request, id):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(instance=instance)
    if request.method=="POST":
        form = PostForm(request.POST, request.FILES, instance=instance)
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

