from django.urls import path
from . import views

urlpatterns = [
	path('', views.home_view, name='home'),
	path('register/', views.register_view, name='register'),
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('profile/', views.profile_view, name='profile'),
	path('', views.PostListView.as_view(), name='post_list'),
	path('posts/', views.PostListView.as_view(), name='post_list'),
	path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
	path('posts/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
	path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
	path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
