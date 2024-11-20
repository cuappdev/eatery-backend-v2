from django.db import models
from user.models import User

class UserSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, related_name="user_sessions", on_delete=models.CASCADE
    )
    session_token = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.netid} - {self.session_token}'