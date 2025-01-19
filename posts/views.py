from urllib.parse import quote_plus
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm

from comments.models import Comment

from .forms import PostForm
from .models import Post

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
            return redirect('posts:detail', slug=instance.slug)
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
    
    
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get_for_model(Post)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
            
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        
        new_comment, created = Comment.objects.get_or_create(
                                user = request.user,
                                content_type=content_type,
                                object_id=obj_id,
                                content=content_data,
                                parent = parent_obj,
                            )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
        
    comments = Comment.objects.filter_by_instance(instance)
    
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, 'posts/post_detail.html', context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_authenticated:
        queryset_list = Post.objects.all() # Can see everything including draft, if user is authenticated
    
    query = request.GET.get("q") # Q = complex lookups
    if query:
        queryset_list = queryset_list.filter( 
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)
                ).distinct() # no duplicate items
    paginator = Paginator(queryset_list, 4) 
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



