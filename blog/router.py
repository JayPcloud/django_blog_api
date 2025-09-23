# from rest_framework import routers
from .viewsets import BlogPostViewSet, BlogMediaViewSet, CommentViewset, LikeViewset, TagViewset, BookMarkViewset
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

app_name = 'blog'

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blogpost')
router.register(r'tags', TagViewset, basename='tag')
# router.register(r'media', BlogMediaViewSet)
# router.register(r'comments', CommentViewset, basename='comment')


blog_router = NestedDefaultRouter(router, r'posts', lookup='blogpost')
blog_router.register(r'likes', LikeViewset, basename='blogpost-likes',)
blog_router.register(r'media', BlogMediaViewSet, basename='blogpost-media',)
blog_router.register(r'comments', CommentViewset, basename='blogpost-comments',)
blog_router.register(r'bookmarks', BookMarkViewset, basename='blogpost-bookmarks',)

urlpatterns = [
    *router.urls,
    *blog_router.urls
]


# blogpost_router = routers.NestedDefaultRouter(router, r'', lookup='blogpost')
# blogpost_router.register(r'media', BlogMediaViewSet, basename='blogmedia')

# urlpatterns = router.urls + blogpost_router.urls