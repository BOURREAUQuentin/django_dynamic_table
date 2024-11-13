import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
import urllib
from .models import DynamicTable, Column, Row, Cell
from django.views.decorators.csrf import csrf_exempt

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
        columns_data = []
        for column in columns:
            columns_data.append({
                'name': column.COL_NAME,
                'type': column.TYD_ID.TYD_FORMAT  # Ajout du type de données
            })
        
        rows_data = []
        for row in rows:
            row_values = []
            for column in columns:
                cell = Cell.objects.filter(COL_ID=column, ROW_ID=row).first()
                cell_value = cell.CEL_VALUE if cell else ""
                row_values.append({
                    'value': cell_value,
                    'type': column.TYD_ID.TYD_FORMAT,  # Ajout du type de données
                    'cel_id': cell.CEL_ID if cell else None
                })
            rows_data.append(row_values)
            
        context = {
            'name': table.TAB_NAME,
            'description': table.TAB_DESCRIPTION,
            'columns': columns_data,
            'rows': rows_data,
            'table_id': table_id,
        }
        
        return render(request, 'dynamictable/tableau.html', context)
    except DynamicTable.DoesNotExist:
        return HttpResponse("Tableau non trouvé", status=404)

@csrf_exempt # désactive CSRF pour les tests locaux. Pense à le retirer en production ou à configurer un token CSRF.
def update_cell(request, cell_id):
    if request.method == "POST":
        try:
            # récupére la nouvelle valeur depuis les données envoyées par le formulaire
            new_value = request.POST.get('new_value')

            if new_value is not None:
                cell = Cell.objects.get(pk=cell_id) # récupérer la cellule avec l'id donné
                cell.CEL_VALUE = new_value # mise à jour de la valeur de la cellule
                cell.save() # sauvegarde la cellule en BD
                return JsonResponse({"status": "success", "new_value": new_value})
            else:
                return JsonResponse({"status": "error", "message": "Missing new_value"}, status=400)

        except Cell.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cell not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def add_row(request, table_id):
    table = DynamicTable.objects.get(TAB_ID=table_id)
    new_row = table.add_default_row()
    print(new_row)

def add_column(request, table_id):
    table = DynamicTable.objects.get(TAB_ID=table_id)
    new_column = table.add_default_column(col_name="Colonne 9")
    print(new_column)
