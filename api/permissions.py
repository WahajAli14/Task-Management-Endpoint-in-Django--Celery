from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project

class IsManager(BasePermission):
    """
    Custom permission to only allow managers to access the view.
    """
    def has_permission(self, request, view):
        user = request.user

        if request.method in SAFE_METHODS:
            # Allow any authenticated user to view
            return user and user.is_authenticated

        # Allow write actions only for managers
        return hasattr(user, 'profile') and user.profile.role == 'manager'

    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(obj, 'project'):  
            project = obj.project
            if(hasattr(project, 'manager')):
                print("Project manager: ", project.manager)
            print("Project: ", project.manager)
        else:  # e.g., Project itself
            project = obj
            print("Else Project: ", project)
        if request.method in SAFE_METHODS:
            
            return obj.project.manager == user or user in obj.project.team_members.all()

        print("User: ", user)
        print("Object: ", obj.project)
        return obj.project.manager == user
    
class IsProjectContributor(BasePermission):
    """
    Custom permission to only allow project contributors to access the view.
    """
    def has_permission(self, request, view):
        user= request.user
        if request.method == "POST":
            project_id = request.data.get("project")
            if not project_id:
                return False  
            try:
                project = Project.objects.get(id=project_id)
                return user == project.manager or user in project.team_members.all()
            except Project.DoesNotExist:
                return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        print("User: ", user)
        print("Object all team members: ", obj.project.team_members.all())
        return obj.project.manager == user or user in obj.project.team_members.all()

class IsCommentAuthorOrReadOnly(BasePermission):
    """
    Allow read access to all users, but only authors can update/delete their comments.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True  # anyone can view
        return obj.author == request.user       