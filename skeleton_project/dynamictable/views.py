from django.shortcuts import render
from django.http import HttpResponse
from .models import DynamicTable, Column, Row, Cell

def home(request):
    return render(request, 'dynamictable/home.html')

def get_dynamic_table_html(request, table_id):
    try:
        # Récupérer le tableau dynamique
        table = DynamicTable.objects.get(TAB_ID=table_id)
        
        # Récupérer les colonnes et les lignes
        columns = Column.objects.filter(TAB_ID=table).order_by('COL_ORDER')
        rows = Row.objects.filter(TAB_ID=table).order_by('ROW_ORDER')
        
        # Préparer les données pour le template
        columns_names = [column.COL_NAME for column in columns]
        rows_data = []
        for row in rows:
            row_values = []
            for column in columns:
                cell = Cell.objects.filter(COL_ID=column, ROW_ID=row).first()
                cell_value = cell.CEL_VALUE if cell else ""
                row_values.append(cell_value)
            rows_data.append(row_values)
        
        # Préparer le contexte pour le template
        context = {
            'name': table.TAB_NAME,
            'description': table.TAB_DESCRIPTION,
            'columns_names': columns_names,
            'rows': rows_data,
        }
        
        # Rendre le template avec le contexte
        return render(request, 'dynamictable/tableau.html', context)
    except DynamicTable.DoesNotExist:
        return HttpResponse("Tableau non trouvé", status=404)

def add_row_dynamic_table(request, tabled_id):
    pass

def add_row_dynamic_table(request, tabled_id):
    pass
