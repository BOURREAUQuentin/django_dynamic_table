from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import DynamicTable, Column, Row, Cell, TypeData
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'dynamictable/home.html')

def get_dynamic_table_html(request, table_id):
    table = get_object_or_404(DynamicTable, TAB_ID=table_id)
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
    
    return render(request, 'dynamictable/table.html', context)

@csrf_exempt # désactive CSRF pour les tests locaux. Penser à le retirer en production ou à configurer un token CSRF.
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
    if request.method == "POST":
        table = get_object_or_404(DynamicTable, TAB_ID=table_id)
        col_name = request.POST.get("name")
        col_type = request.POST.get("type")

        # Vérifier le type de donnée de la colonne
        type_data = TypeData.objects.filter(TYD_NAME=col_type).first()
        if not type_data:
            return JsonResponse({"success": False, "error": "Type de donnée non trouvé"}, status=400)

        table.add_column(col_name=col_name, typ_name=col_type)

        return get_dynamic_table_html(request, table_id)
