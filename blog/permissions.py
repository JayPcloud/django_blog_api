from rest_framework import permissions

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in ['POST', 'GET']:
            return True
        
        user = request.user

        author = getattr(obj, 'author', None)

        # If there's no direct author, try via blog relation
        if not author:
            blog = getattr(obj, 'blog_post', None)
            if blog:
                author = getattr(blog, 'author', None)
        

        return author == user
    

class NoUpdate(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.method in ['PUT', 'PATCH']
    

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class NoDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.method == 'DELETE'   

        