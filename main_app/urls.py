from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.posts_index, name='home'),
  path('about/', views.about, name='about'),
  path('posts/', views.posts_index, name='index'),
  path('posts/<int:post_id>/', views.posts_detail, name='detail'),
  path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
  path('posts/create/', views.PostCreate.as_view(), name='posts_create'),
  path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
  path('accounts/', include('django.contrib.auth.urls')),

  path('acconts/signup', views.signup, name='signup'),
  path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
  path('profile/', views.get_user_profile, name='get_user_profile'),
  path('profile/change_password', views.change_password, name='change_password'),
  path('profile/change_username', views.change_username, name='change_username'),
]