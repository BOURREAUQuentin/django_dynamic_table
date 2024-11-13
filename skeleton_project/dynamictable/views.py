from django.shortcuts import render
from django.http import HttpResponse
from .models import DynamicTable, Column, Row, Cell,TypeData
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string


def home(request):
    return render(request, 'dynamictable/home.html')

def get_dynamic_table_html(request, table_id):
    table = get_object_or_404(DynamicTable, TAB_ID=table_id)
    columns = table.column_set.all().order_by('COL_ORDER')
    rows = Row.objects.filter(TAB_ID=table).all()

    rows_data = []
    for row in rows:
        cells = row.cell_set.all().order_by('COL_ID')  # Trier les cellules par ordre de colonne
        rows_data.append(cells)

    context = {
        'columns_names': columns,
        'rows': rows_data,
    }

    return render(request, 'dynamictable/tableau.html', context)

def add_column_to_table(request, table_id):
    if request.method == "POST":
        table = get_object_or_404(DynamicTable, TAB_ID=table_id)
        col_name = request.POST.get("name")
        col_type = request.POST.get("type")

        # Récupérer le type de donnée de la colonne
        type_data = TypeData.objects.filter(TYD_NAME=col_type).first()
        if not type_data:
            return JsonResponse({"success": False, "error": "Type de donnée non trouvé"}, status=400)

        # Créer la nouvelle colonne
        col_order = Column.objects.filter(TAB_ID=table).count() + 1
        new_column = Column.objects.create(
            COL_NAME=col_name,
            COL_ORDER=col_order,
            TAB_ID=table,
            TYD_ID=type_data
        )

        # Ajouter une cellule vide pour chaque ligne existante
        rows = Row.objects.filter(TAB_ID=table).all()
        for row in rows:
            Cell.objects.create(CEL_VALUE="", COL_ID=new_column, ROW_ID=row)
        

        # Récupérer toutes les colonnes mises à jour et les lignes
        columns = table.column_set.all().order_by('COL_ORDER')
        rows_data = []
        rows = Row.objects.filter(TAB_ID=table).all()

        for row in rows:
            cells = row.cell_set.all().order_by('COL_ID')
            rows_data.append(cells)
        
        print("columns", columns)

        # Préparer le contexte pour rendre l'intégralité du tableau avec les nouvelles colonnes
        context = {
            'name': table.TAB_NAME,
            'description': table.TAB_DESCRIPTION,
            'columns_names': columns,
            'rows': rows_data,
        }

        # Retourner l'intégralité du tableau mis à jour
        return render(request, 'dynamictable/partials/dynamic_table_body.html', context)

    return JsonResponse({"success": False}, status=400)






def add_row_dynamic_table(request, tabled_id):
    pass
