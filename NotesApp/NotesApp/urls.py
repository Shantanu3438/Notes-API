from django.urls import path
from Notes import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('notes/create/', views.createNote, name='createNote'),
    path('notes/<int:pk>/delete/', views.deleteNote, name='deleteNote'),
    path('notes/<int:pk>/', views.getNote, name='getNote'),
    path('notes/<int:pk>/update/', views.updateNote, name='updateNote'),

]