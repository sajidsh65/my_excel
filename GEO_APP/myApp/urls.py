from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    # path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('generate_excel/', views.generate_excel, name='generate_excel'),
    path('add_info/<int:row>/', views.add_info, name='add_info'),
    path('download/', views.download_excel, name='download_excel'),
]
