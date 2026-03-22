from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=280, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return(self.message)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=280, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    from_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
