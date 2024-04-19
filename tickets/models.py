from django.db import models
from django.conf import settings

class maintickets(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], default='open')
    file_content = models.BinaryField(null=True, blank=True, editable=True)  # Ensure this is editable
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)#he MIME type
    def __str__(self):
        return self.title
