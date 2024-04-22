from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group

class maintickets(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], default='open')
    file_content = models.BinaryField(null=True, blank=True, editable=True)  # Ensure this is editable
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)#he MIME type
    assigned_team = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    assigned_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')

    def __str__(self):
        return self.title
class Comment(models.Model):
    ticket = models.ForeignKey(maintickets, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.created_at}'