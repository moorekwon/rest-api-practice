from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail)
]
