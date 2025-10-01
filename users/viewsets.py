from rest_framework import viewsets, mixins, serializers, status, permissions
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, PrivateUserSerializer, PublicUserSerializer
from .models import Profile
from .permissions import IsUserOwnerOrGetAndPostOnly,IsUserOwnerOrGetOnly,NoPost
from blog.models import BlogPost, BookMark, Notification
from blog.serializers import BlogPostSerializer,BookMarkSerializer, NotificationSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from blog.permissions import ReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

class UsersViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [IsUserOwnerOrGetAndPostOnly,]
    lookup_field = 'pk' 


    def get_serializer_class(self):
        if self.action == 'retrieve' and self.request.user == self.get_object():
            return PrivateUserSerializer
        return PublicUserSerializer
    

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to view all users.")
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='reset-admin-password')
    def reset_admin_password(self, request):
        try:
            user = User.objects.get(username='admin')  # Change if needed
            user.set_password('NewSecurePassword123!')
            user.save()
            return Response({'status': '✅ Password reset successful'})
        except User.DoesNotExist:
            return Response({'status': '❌ Admin user not found'}, status=404)
        
    

class ProfileViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
    ):
    queryset=Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsUserOwnerOrGetOnly,]


class UserBlogViewset(viewsets.ModelViewSet):
    queryset=BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsUserOwnerOrGetOnly, NoPost]
    
    def get_queryset(self):
        blog_pk = self.kwargs.get('user_pk')
        try:
            user = User.objects.get(pk=blog_pk)
        except User.DoesNotExist:
            raise NotFound(f"No user associated with the id:{blog_pk}")
        
        return user.blog_posts.all()


class UserBookMarkedBlogViewset(viewsets.ModelViewSet):
    queryset=BookMark.objects.all()
    serializer_class = BookMarkSerializer
    permission_classes = [IsUserOwnerOrGetOnly, NoPost]
    
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if not int(user_pk) == self.request.user.pk:
            raise PermissionDenied(detail='You only have access to your own bookmarked posts')
        return self.request.user.bookmarks.all()
    
    
    
class UserNotificationViewset(viewsets.ModelViewSet):
    queryset=Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]
    
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if not int(user_pk) == self.request.user.pk:
            raise PermissionDenied(detail='You only have access to your own notifications')
        return self.request.user.notifications.all().order_by('-created_at')
    


        