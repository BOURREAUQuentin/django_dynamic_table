from django.urls import path
from . import views

app_name = 'dynamictable'

urlpatterns = [
    path('', views.home, name='home'),
    path('table/<int:table_id>/', views.get_dynamic_table_html, name='dynamictable'),
    path('table/<int:table_id>/add_column/', views.add_column, name='add_column'),
    path('table/<int:table_id>/add_row/', views.add_row, name='add_row'),
    path('table/update_cellule/<int:cell_id>/', views.update_cell, name='update_cell'),
    path('table/delete_column/<int:table_id>/<int:column_id>/', views.delete_column, name='delete_column'),
    path('table/delete_row/<int:table_id>/<int:row_id>/', views.delete_row, name='delete_row'),
    path('table/update_column/<int:table_id>/<int:column_id>/', views.update_column, name='update_column')
    ]