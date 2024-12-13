from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.viewPosts),
    path('addpost/', views.addPost),
    path('posts/<str:pk>/', views.viewPostDetail),
    path('updatepost/<str:pk>/', views.updatePost),
    path('delete/<str:pk>/', views.deletePost),
]