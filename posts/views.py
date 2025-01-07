from urllib.parse import quote_plus
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm

# Create your views here.
def post_create(request):
    if not request.user.is_authenticated:
        raise Http404
    
    form = PostForm()
    if request.method=="POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
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
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_authenticated:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string
    }
    return render(request, 'posts/post_detail.html', context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_authenticated:
        queryset_list = Post.objects.all() # Can see everything including draft
    paginator = Paginator(queryset_list, 25) 

    page_number = request.GET.get("page")
    queryset = paginator.get_page(page_number)
    context = {
            "object_list": queryset,
            "title": "List", 
            "today": today
        }
    return render(request, 'posts/post_list.html', context)


def post_update(request, slug):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=instance)  
    if request.method=="POST":
        form = PostForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Item Saved", extra_tags='some-tag')
            return redirect('posts:detail', slug=slug)
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    
    return render(request, 'posts/post_update.html', context)

def post_delete(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")   
    return redirect('posts:list')

