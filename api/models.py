from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('qa', 'QA'),
        ('developer', 'Developer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    team_members = models.ManyToManyField(User, related_name='projects')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects',null=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('review', 'Review'),
        ('working', 'Working'),
        ('awaiting_release', 'Awaiting Release'),
        ('waiting_qa', 'Waiting QA'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.title} [{self.status}]"


class Document(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='documents/')
    version = models.CharField(max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return f"{self.name} (v{self.version})"


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.created_at}"


