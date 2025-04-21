from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .permissions import IsManager, IsProjectContributor, IsCommentAuthorOrReadOnly
from .models import Profile, Project, Task, Document, Comment
from .utils import get_tokens_for_user
from .serializer import (
    ProfileSerializer, ProjectSerializer, TaskSerializer,
    DocumentSerializer, CommentSerializer ,RegisterSerializer
)
from .tasks import sample_task

class RunSampleTaskView(APIView):
    def get(self, request):
        sample_task.delay()
        return Response({"message": "Task is running in the background."})
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    
    def get_queryset(self):
        user= self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'manager':
            return Project.objects.filter(manager=user)
        return Project.objects.filter(team_members=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)
    # def create(self, request, *args, **kwargs):
    #     user = request.user

    #     if not self.is_manager(request.user):
    #         return Response(
    #             {"detail": "Only managers can create projects."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     return super().create(request, *args, **kwargs)
    
    # def update(self, request, *args, **kwargs):
    #     user = request.user

    #     if not self.is_manager(request.user):
    #         return Response(
    #             {"detail": "Only managers can create projects."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     return super().update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     user = request.user

    #     if not self.is_manager(request.user):
    #         return Response(
    #             {"detail": "Only managers can create projects."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     return super().destroy(request, *args, **kwargs)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    
    def perform_create(self, serializer):
        serializer.save(assignee=None)
    
    @action(detail=True, methods=['post'], url_path='assign')
    def assign_task(self, request, pk=None):
        
        task = self.get_object()
        username = request.data.get("assignee")

        if not username:
            return Response({"detail": "Assignee username is required."}, status=400)

        try:
            assignee = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        # ✅ Check if assignee is a team member of the task's projec
        if assignee not in task.project.team_members.all():
            return Response({"detail": "Assignee must be a team member of the project."}, status=403)

        task.assignee = assignee
        task.save()

        return Response({"detail": f"Task assigned to {username} successfully."}, status=200) 
 
        
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor ]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthorOrReadOnly]
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        task_id = self.request.query_params.get('task')
        project_id = self.request.query_params.get('project')

        if task_id:
            queryset = queryset.filter(task__id=task_id)
        elif project_id:
            queryset = queryset.filter(project__id=project_id)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                 'user': {
                    'username': user.username,
                    'email': user.email,
                    'role': user.profile.role,
                    'contact_number': user.profile.contact_number
                },
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token= RefreshToken(refresh_token)
            token.blacklist()
            return Response({'ok': 'token is blacklisted'},status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': "Invalid token"},status=status.HTTP_400_BAD_REQUEST)        
        
