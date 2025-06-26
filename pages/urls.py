from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    ProjectDetailView,
    BlogDetailView,
    BlogListView,
    ProjectListView,
    health_check,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('aboutme/', AboutPageView.as_view(), name='aboutme'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('health/', health_check, name='health_check'),
]   
