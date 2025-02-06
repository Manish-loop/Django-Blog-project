from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView, 
    RetrieveAPIView, 
    DestroyAPIView, 
    RetrieveUpdateAPIView
    )


from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
    )

from posts.models import Post

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

from .permissions import IsOwnerOrReadOnly

from posts.api.serializers import (
    PostCreateUpdateSerializer, 
    PostListSerializer, 
    PostDetailSerializer
    )

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

  
class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes= [AllowAny]
    search_fields = ['title', 'content', 'user__first_name']
    pagination_class = PostPageNumberPagination 

    def get_queryset(self, *args, **kwargs):  # overridding get default method 
        queryset_list = Post.objects.all() # filter(user=self.request.user)
        query = self.request.GET.get("q") # Q = complex lookups #since, it is class-based views so self is required
        if query:
            queryset_list = queryset_list.filter( 
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query)|
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list
    