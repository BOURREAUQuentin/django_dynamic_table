from django.urls import path
from . import views

app_name = 'dynamictable'

urlpatterns = [
    path('', views.home, name='home'),
    path('tableau/<int:table_id>/', views.get_dynamic_table_html, name='dynamictable'),
    path('table/<int:table_id>/add_column/', views.add_column_to_table, name='add_column_to_table'),]