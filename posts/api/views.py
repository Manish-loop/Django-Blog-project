from rest_framework.generics import ListAPIView

from posts.models import Post

class PostListView(ListAPIView):
    queryset = Post.objects.all()


    # def get_queryset()  # customize how that works by overriding the get_queryset method
