from django.urls import path
from .views import MenuList, MenuDetail

urlpatterns = [
    path('menus/', MenuList.as_view()),
    path('menus/<str:id>/', MenuDetail.as_view()),
]