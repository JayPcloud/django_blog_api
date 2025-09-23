from rest_framework.throttling import UserRateThrottle

class BlogCreateBurstThrottle(UserRateThrottle):
    scope = 'blog_create_burst'

class BlogCreateSustainedThrottle(UserRateThrottle):
    scope = 'blog_create_sustained'

class MediaCreateBurstThrottle(UserRateThrottle):
    scope = 'media_create_burst'

class MediaCreateSustainedThrottle(UserRateThrottle):
    scope = 'media_create_sustained'

class CommentCreateBurstThrottle(UserRateThrottle):
    scope = 'comment_create_burst'

class CommentCreateSustainedThrottle(UserRateThrottle):
    scope = 'comment_create_sustained'