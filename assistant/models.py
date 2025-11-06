from django.db import models

class UserSession(models.Model):
    USER_TYPE_CHOICES = [
        ('blind', 'Blind User'),
        ('deaf', 'Deaf User'),
        ('unknown', 'Unknown')
    ]
    
    session_id = models.CharField(max_length=100, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='unknown')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.session_id} - {self.user_type}"

class Conversation(models.Model):
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='conversations')
    message = models.TextField()
    is_user = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.session.session_id} - {'User' if self.is_user else 'Assistant'}"