from rest_framework import serializers
from .models import Profile, Project, Task, Document, Comment, CustomUser

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
                         
class ProfileSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'role', 'contact_number']


class ProjectSerializer(serializers.ModelSerializer):
    team_members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all()
    )
   

    class Meta:
        model = Project
        fields = '__all__'

    

class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(
            queryset=CustomUser.objects.all(),
            required=False
        )
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project', 'assignee']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['assignee_name'] = instance.assignee.first_name + ' ' + instance.assignee.last_name if instance.assignee else None
        return rep
    
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'description', 'file', 'version', 'project']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

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
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES)
    contact_number = serializers.CharField(max_length=15)
   
    def create(self, validated_data):
        role= validated_data.pop('role')
        contact_number= validated_data.pop('contact_number')
        user= CustomUser.objects.create_user(**validated_data)
        Profile.objects.create(user=user, role=role, contact_number=contact_number)
        return user
