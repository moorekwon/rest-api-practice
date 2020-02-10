from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail)
]

# 패턴 추가하여 사용자가 원하는 형태의 포맷을 전달받기
urlpatterns = format_suffix_patterns(urlpatterns)
