from rest_framework import viewsets
from .models import BlogPost,BlogMedia, Comment, Like, Tag, BookMark, Notification
from .serializers import BlogPostSerializer,BlogMediaSerializer, CommentSerializer, LikeSerializer, TagSerializer, BookMarkSerializer, NotificationSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly, NoUpdate, ReadOnly, NoDelete
from rest_framework import permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .throttles import BlogCreateBurstThrottle, BlogCreateSustainedThrottle, MediaCreateBurstThrottle, MediaCreateSustainedThrottle, CommentCreateBurstThrottle, CommentCreateSustainedThrottle
import datetime
from .pagination import BlogPagination


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrGetAndPostOnly,]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'tags']
    throttle_classes = [BlogCreateBurstThrottle, BlogCreateSustainedThrottle]
    pagination_class = BlogPagination

    class BlogPostFilter(filters.FilterSet):
        created_at = filters.DateFromToRangeFilter()
        created_today = filters.BooleanFilter(method='filter_created_today')
        created_yesterday = filters.BooleanFilter(method='filter_created_yesterday')
        created_this_week = filters.BooleanFilter(method='filter_created_this_week')

        class Meta:
            model = BlogPost
            fields = ['author', 'tags', 'created_at']

        def filter_created_today(self, queryset, name, value):
            if value:
                today = datetime.date.today()
                return queryset.filter(created_at__date=today)
            return queryset

        def filter_created_yesterday(self, queryset, name, value):
            if value:
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                return queryset.filter(created_at__date=yesterday)
            return queryset

        def filter_created_this_week(self, queryset, name, value):
            if value:
                today = datetime.date.today()
                start_week = today - datetime.timedelta(days=today.weekday())
                return queryset.filter(created_at__date__gte=start_week)
            return queryset

    filterset_class = BlogPostFilter
    search_fields = ['title', 'content', 'tags',]
    ordering_fields = ['created_at', 'title',]
    throttle_classes = [BlogCreateBurstThrottle, BlogCreateSustainedThrottle,]
    
    @action(detail=True, methods=['post','get'], permission_classes=[permissions.IsAuthenticated])
    def toggle_like(self, request, pk=None):
        blog = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(blog=blog, user=user)

        if not created:
            like.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post','get'], permission_classes=[permissions.IsAuthenticated])
    def toggle_bookmark(self, request, pk=None):
        blog = self.get_object()
        user = request.user

        bookmarked, created = BookMark.objects.get_or_create(blog=blog, user=user)

        if not created:
            bookmarked.delete()
            return Response({"message": "bookmark removed"}, status=status.HTTP_200_OK)
        
        return Response({"message": "bookmarked"}, status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    
    def get_throttles(self):
        if self.request.method == 'POST':
            return [throttle() for throttle in self.throttle_classes]
        return []


class BlogMediaViewSet(viewsets.ModelViewSet):
    queryset = BlogMedia.objects.all()
    serializer_class = BlogMediaSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrGetAndPostOnly, NoUpdate, NoDelete]
    throttle_classes = [MediaCreateBurstThrottle, MediaCreateSustainedThrottle,]


    def get_queryset(self):
        blogpost_pk = self.kwargs.get('blogpost_pk')
        if blogpost_pk:
            return BlogMedia.objects.filter(blog_post=blogpost_pk)
        return BlogMedia.objects.none()

    def perform_create(self, serializer):
        blogpost_pk = self.kwargs.get('blogpost_pk')
    
        try:
            blog_post = BlogPost.objects.get(id=blogpost_pk)
        except BlogPost.DoesNotExist: 
            raise serializers.ValidationError("Blog does not exist")
        
        if not self.request.user == blog_post.author:
            raise serializers.ValidationError({"Permission denied": "Only this Blog's author is allowed to perform this action"})
       
        serializer.save(blog_post = blog_post)
        
    
    def get_throttles(self):
        if self.request.method == 'POST':
            return [throttle() for throttle in self.throttle_classes]
        return []
    
    
    
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrGetAndPostOnly, NoUpdate,]
    throttle_classes = [CommentCreateBurstThrottle, CommentCreateSustainedThrottle,]
    
    def get_queryset(self):
        blogpost_pk = self.kwargs.get('blogpost_pk')
        if blogpost_pk:
            query_set = Comment.objects.filter(blog=blogpost_pk)
            
            parent_comment_id = self.request.query_params.get('parent_comment_id')
            
            if parent_comment_id:
                try:
                    parent = Comment.objects.get(pk=parent_comment_id)
                except Comment.DoesNotExist:
                    raise NotFound(f"Comment with id:{parent_comment_id} does not exist")
                return query_set.filter(parent=parent)
            
            return query_set.filter(parent__isnull=True)
            
        return Comment.objects.none()
    

    def perform_create(self, serializer):
        blogpost_pk = self.kwargs.get('blogpost_pk')
        
        try:
            blog = BlogPost.objects.get(id=blogpost_pk)
        except BlogPost.DoesNotExist: 
            raise serializers.ValidationError("Blog does not exist")
        
        comment_id = self.request.query_params.get('parent_comment_id')
        
        parent = None
        
        if comment_id:
            try:
                parent = Comment.objects.get(pk=comment_id)
                if parent.parent is not None:
                    raise serializers.ValidationError("You can only reply to top-level comments.")
            except Comment.DoesNotExist:
                raise NotFound(f"Comment with id:{comment_id} does not exist")
        
        serializer.save(author=self.request.user, blog = blog, parent=parent)
        
    
    def get_throttles(self):
        if self.request.method == 'POST':
             return [throttle() for throttle in self.throttle_classes]
        return []
    



class LikeViewset(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]
    # parent_lookup_kwargs = {'blogpost_pk': 'blog__pk'}  # <-- Add this line

    def get_queryset(self):
        blogpost_pk = self.kwargs.get('blogpost_pk')
        if blogpost_pk:
            return Like.objects.filter(blog=blogpost_pk)
        return Like.objects.none()
    


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [ReadOnly]
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name',]


class BookMarkViewset(viewsets.ModelViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly,]
    # parent_lookup_kwargs = {'blogpost_pk': 'blog__pk'}  # <-- Add this line

    def get_queryset(self):
        blogpost_pk = self.kwargs.get('blogpost_pk')
        if blogpost_pk:
            return BookMark.objects.filter(blog=blogpost_pk)
        return BookMark.objects.none()
    
    
class NotificationViewset(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly,]
    
    def get_queryset(self):
        return self.request.user.notifications
    
    
