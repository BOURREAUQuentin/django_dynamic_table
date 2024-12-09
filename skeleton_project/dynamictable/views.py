import logging
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
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
            'type': column.TYD_ID.TYD_FORMAT,  # Ajout du type de données
            'column_order': column.COL_ORDER,
            'id_column': column.COL_ID
        })
    
    rows_data = []
    for row in rows:
        row_values = {
            'ROW_ID': row.ROW_ID,
            'values': []
        }
        for column in columns:
            cell = Cell.objects.filter(COL_ID=column, ROW_ID=row).first()
            cell_value = cell.CEL_VALUE if cell else ""
            row_values['values'].append({
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

        table.add_column(col_name=col_name, typ_name=col_type, )
        context = load_dynamic_table_context(table_id)
        return render(request, 'dynamictable/dynamic_table_body.html', context)


def load_dynamic_table_context(table_id):
    table = get_object_or_404(DynamicTable, TAB_ID=table_id)
    columns = Column.objects.filter(TAB_ID=table).order_by('COL_ORDER')
    rows = Row.objects.filter(TAB_ID=table).order_by('ROW_ORDER')
    
    
    # Préparer les données pour le template
    columns_data = []
    for column in columns:
        columns_data.append({
            'name': column.COL_NAME,
            'type': column.TYD_ID.TYD_FORMAT,  # Ajout du type de données
            'column_order': column.COL_ORDER,
            'id_column': column.COL_ID
        })
    
    rows_data = []
    for row in rows:
        row_values = {
            'ROW_ID': row.ROW_ID,
            'values': []
        }
        for column in columns:
            cell = Cell.objects.filter(COL_ID=column, ROW_ID=row).first()
            cell_value = cell.CEL_VALUE if cell else ""
            row_values['values'].append({
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
    
    return context

def delete_column(request, table_id, column_id):
    print(f"Received table_id: {table_id}, column_id: {column_id}")
    # Récupérer la colonne à supprimer
    column = get_object_or_404(Column, COL_ID=column_id, TAB_ID=table_id)
    
    print(column.COL_ORDER)
    # Supprimer les cellules associées à cette colonne
    Cell.objects.filter(COL_ID=column).delete()
    
    # Supprimer la colonne elle-même
    column.delete()
    
    remaining_columns = Column.objects.filter(TAB_ID=table_id).order_by('COL_ORDER')
    for new_order, col in enumerate(remaining_columns, start=1):
        col.COL_ORDER = new_order
        col.save()

    context = load_dynamic_table_context(table_id)
    return render(request, 'dynamictable/dynamic_table_body.html', context)


def delete_row(request, table_id, row_id):
    print(f"Received table_id: {table_id}, row_id: {row_id}")
    # Récupérer la colonne à row
    row = get_object_or_404(Row, ROW_ID=row_id, TAB_ID=table_id)
    
    
    # Supprimer les cellules associées à cette row
    Cell.objects.filter(ROW_ID=row).delete()
    
    # Supprimer la row elle-même
    row.delete()
    
    remaining_row = Row.objects.filter(TAB_ID=table_id).order_by('ROW_ORDER')
    for new_order, row in enumerate(remaining_row, start=1):
        row.ROW_ORDER = new_order
        row.save()

    context = load_dynamic_table_context(table_id)
    return render(request, 'dynamictable/dynamic_table_body.html', context)



@csrf_exempt  # À retirer ou ajuster pour les environnements de production
def update_column(request, table_id, column_id):
    if request.method == "POST":
        try:
            # Récupérer les données POST
            column_name = request.POST.get("column_name")
            column_type = request.POST.get("column_type")

            # Valider que les champs nécessaires sont présents
            if not column_name or not column_type:
                return JsonResponse({"status": "error", "message": "Missing column_name or column_type"}, status=400)

            # Vérifier si la colonne existe
            column = Column.objects.filter(COL_ID=column_id, TAB_ID=table_id).first()
            if not column:
                return JsonResponse({"status": "error", "message": "Column not found"}, status=404)

            # Vérifier si le type de données est valide
            type_data = TypeData.objects.filter(TYD_NAME=column_type).first()
            if not type_data:
                return JsonResponse({"status": "error", "message": f"Invalid column type: {column_type}"}, status=400)

            # Mettre à jour la colonne
            column.COL_NAME = column_name
            column.TYD_ID = type_data
            column.save()

            # Réponse de succès
            context = load_dynamic_table_context(table_id)
            return render(request, 'dynamictable/dynamic_table_body.html', context)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # Réponse pour une méthode non autorisée
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
