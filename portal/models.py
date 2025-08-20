
from django.db import models
from django.utils import timezone

class Teacher(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_salt = models.CharField(max_length=64)  # hex
    password_hash = models.CharField(max_length=128) # hex pbkdf2
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class SessionToken(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)  # hex
    user_agent_hash = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    marks = models.PositiveIntegerField()

    class Meta:
        unique_together = ('name', 'subject')

    def __str__(self):
        return f"{self.name} - {self.subject}"

class AuditLog(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # create/update/delete/login
    details = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
