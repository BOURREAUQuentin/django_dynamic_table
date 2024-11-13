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

@csrf_exempt  # Désactive CSRF pour les tests locaux. Pense à le retirer en production ou à configurer un token CSRF.
def update_cell(request, cell_id):
    if request.method == "PUT":
        # Décoder le corps de la requête en chaîne de caractères
        body = request.body.decode('utf-8')  # Décoder en 'utf-8'

        # Utiliser parse_qs pour analyser les données encodées en 'application/x-www-form-urlencoded'
        data = urllib.parse.parse_qs(body)

        # Récupérer la valeur de la clé 'cell_id'
        new_value = data.get(str(cell_id), [None])[0]  # Si 'cell_id' n'existe pas, retourner None
        
        if new_value:
            # Traitement de la valeur, ici mise à jour de la cellule par exemple
            try:
                # Imaginons que tu mets à jour une cellule avec cette valeur
                cell = Cell.objects.get(pk=cell_id)
                cell.CEL_VALUE = new_value
                cell.save()

                return JsonResponse({"status": "success", "new_value": new_value})
            except Cell.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Cell not found"}, status=404)
        else:
            return JsonResponse({"status": "error", "message": "Missing new_value"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def add_row(request, table_id):
    table = DynamicTable.objects.get(TAB_ID=table_id)
    new_row = table.add_default_row()
    print(new_row)

def add_column(request, table_id):
    table = DynamicTable.objects.get(TAB_ID=table_id)
    new_column = table.add_default_column(col_name="Colonne 9")
    print(new_column)
