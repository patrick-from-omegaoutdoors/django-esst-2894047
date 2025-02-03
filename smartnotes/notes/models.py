from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="notes",
    )
