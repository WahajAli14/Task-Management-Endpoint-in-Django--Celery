from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Project, Task, Document, Comment

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
                         
class ProfileSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'role', 'contact_number']


class ProjectSerializer(serializers.ModelSerializer):
    team_members = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='username'
    )
   

    class Meta:
        model = Project
        fields = '__all__'

    

class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.SlugRelatedField(read_only=True,
            slug_field='username'
        )
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project', 'assignee']

    
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'description', 'file', 'version', 'project']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at', 'task', 'project']
        read_only_fields = ['created_at']

    def validate(self, attrs):
        if not attrs.get('task') and not attrs.get('project'):
            raise serializers.ValidationError("Either task or project must be provided.")
        if attrs.get('task') and attrs.get('project'):
            raise serializers.ValidationError("Only one of task or project can be provided.")
        return attrs
        
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role= serializers.ChoiceField(choices=Profile.ROLE_CHOICES)
    contact_number= serializers.CharField(max_length=15)
   
    def create(self, validated_data):
        print("Validated Data " , validated_data)
        role= validated_data.pop('role')
        contact_number= validated_data.pop('contact_number')
        user= User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, role=role, contact_number=contact_number)
        return user
