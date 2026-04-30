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

class Perfil(models.Model):
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=280, blank=True)
    profile_picture = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_relationships")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_relationships")
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    profile_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('profile_user', 'post')


