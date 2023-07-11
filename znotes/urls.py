from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register/', views.register, name='register'),
    path('notes/<int:id>/', views.shownotes, name='shownotes'),
    path('dept/<str:deptname>/', views.dept, name='dept'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('uploadnotes/', views.uploadnotes, name='uploadnotes'),
    path('showall/<int:id>/', views.showall, name='showall'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(),name = "delete"),
    path('search/', views.search, name='search'),

]
