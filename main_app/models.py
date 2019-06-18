from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=100)
  date = models.DateField('Post Date', default='2020-01-01')
  time = models.CharField(max_length=100, default='')
  address = models.CharField(max_length=250, default='Austin, TX')
  category = models.CharField(max_length=100, default='Food')
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