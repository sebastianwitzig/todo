from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from todo_app.views import ToDoViewSet

router = routers.DefaultRouter()
router.register('todos', ToDoViewSet, basename='todos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include((router.urls, 'todo_app'), namespace='api'))
]
