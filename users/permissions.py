from rest_framework import permissions

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == "POST" and not request.user.is_authenticated:
            return True
        
        if request.method == "POST" and request.user.is_authenticated:
            return False
        
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        
        if request.method == "POST":
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user == obj
        

class IsUserOwnerOrGetOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and  request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        author = getattr(obj, 'author', None)
        
        if author:
            return request.user == obj.author
        
        return request.user == obj.user
    
    
class NoPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.method == 'POST'
           
        