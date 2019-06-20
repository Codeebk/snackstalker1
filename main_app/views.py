from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import uuid
import boto3
from .models import Post, Photo

# from django.http import 
S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'ushio'
# BUCKET = 'catcollector9'




class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = ['title', 'date', 'time', 'address', 'category', 'description']  

# Class views
class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'date', 'time', 'address', 'category', 'description']
   
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/posts/'


# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def posts_index(request):
  posts = Post.objects.all().order_by('date')
  return render(request, 'posts/index.html', {'posts': posts})

def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  return render(request, 'posts/detail.html', {'post': post})

def get_user_profile(request):
  posts = Post.objects.filter(user=request.user)
  return render(request, 'main_app/user_profile.html', {'posts': posts})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_photo(request, post_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        # build the full url string
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        # we can assign to cat_id or cat (if you have a cat object)
        photo = Photo(url=url, post_id=post_id)
        photo.save()
      except:
        print('An error occurred uploading file to S3')
    return redirect('detail', post_id=post_id)  
  
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('get_user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

def change_username(request):
    if request.method == 'POST':
        form = UserChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # update_session_auth_hash(request, user) 
            return redirect('get_user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
      form = UserChangeForm(request.user)
    return render(request, 'registration/change_username.html', {'form': form})

