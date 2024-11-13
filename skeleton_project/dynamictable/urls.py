from django.urls import path
from . import views

app_name = 'dynamictable'

urlpatterns = [
    path('', views.home, name='home'),
    path('tableau/<int:table_id>/', views.get_dynamic_table_html, name='dynamictable'),
    path('tableau/<int:table_id>/add_column/', views.add_column, name='add_column'),
    path('tableau/<int:table_id>/add_row/', views.add_row, name='add_row'),
    path('tableau/update_cellule/<int:cell_id>/', views.update_cell, name='update_cell'),
]