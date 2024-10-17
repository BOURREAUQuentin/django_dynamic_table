from django.urls import path
from . import views

app_name = 'dynamictable'

urlpatterns = [
    path('', views.home, name='home'),
    path('tableau/<int:table_id>/', views.get_dynamic_table_html, name='dynamictable'),
]