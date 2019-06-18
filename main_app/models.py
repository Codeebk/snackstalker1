from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('detail', kwargs={'post_id': self.id})

class Photo(models.Model):
  url = models.CharField(max_length=200)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)

  def __str__(self):
      return f"Photo for post_id: {self.post_id} @{self.url}" 