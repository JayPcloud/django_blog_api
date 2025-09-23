from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .viewsets import UsersViewSet,ProfileViewSet,UserBlogViewset, UserBookMarkedBlogViewset, UserNotificationViewset

app_name = 'users'

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='user')
router.register('profile', ProfileViewSet)

user_blog_nested_router = NestedDefaultRouter(router, r'users', lookup='user')
user_blog_nested_router.register(r'blogs', UserBlogViewset, basename='user-blogs',)
user_blog_nested_router.register(r'bookmarks', UserBookMarkedBlogViewset, basename='user-bookmarks',)
user_blog_nested_router.register(r'notifications', UserNotificationViewset, basename='user-notifications',)

urlpatterns = [
    *router.urls,
    *user_blog_nested_router.urls
]