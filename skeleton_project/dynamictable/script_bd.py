# python3 manage.py shell < dynamictable/script_bd.py

from dynamictable.models import *
from datetime import timedelta

# Suppression de toutes les données existantes
print("Nettoyage de la base de données...")

# Supprimer dans l'ordre pour respecter les contraintes de clés étrangères
Cell.objects.all().delete()
Row.objects.all().delete()
TagOption.objects.all().delete()
Column.objects.all().delete()
DynamicTable.objects.all().delete()
Support.objects.all().delete()
Project.objects.all().delete()
Document.objects.all().delete()
Artist.objects.all().delete()
Category.objects.all().delete()
TypeData.objects.all().delete()
Employee.objects.all().delete()

print("Base de données nettoyée. Création des nouvelles données...")

# Créer une catégorie
category = Category.objects.create(CAT_NAME="Projet Web")

# Créer un artiste
artist = Artist.objects.create(
    ART_NAME="JohnDoe",
    ART_FIRSTNAME="John",
    ART_LASTNAME="Doe",
    ART_EMAIL="john.doe@example.com",
    ART_TEL="1234567890",
    ART_PASSWORD="password123",
    ART_BIOGRAPHY="Un artiste talentueux"
)

# Créer un document
document = Document.objects.create(
    DOC_NAME="Site Web E-commerce",
    DOC_INFORMATION="Création d'un site web e-commerce",
    ART_ID=artist
)
document = Document.objects.create(
    DOC_NAME="Suivi des bugs",
    DOC_INFORMATION="Document pour suivre les bugs du projet e-commerce",
    ART_ID=artist
)

# Créer un projet
project = Project.objects.create(
    PRJ_NAME="E-commerce 2024",
    PRJ_FORMAT="Web",
    PRJ_DUE_DATE="2024-12-31",
    DOC_ID=document
)

# Créer un support
support = Support.objects.create(
    SUP_NAME="Développement Frontend",
    SUP_DURATION=timedelta(days=14),  # 14 jours
    SUP_PROGRESS=0.0,
    PRJ_ID=project,
    CAT_ID=category
)
support = Support.objects.create(
    SUP_NAME="Suivi des bugs",
    SUP_DURATION=timedelta(days=30),  # 30 jours
    SUP_PROGRESS=0.0,
    PRJ_ID=project,
    CAT_ID=category
)

# Créer des types de données
type_text = TypeData.objects.create(TYD_NAME="Texte", TYD_FORMAT="string")
type_number = TypeData.objects.create(TYD_NAME="Nombre", TYD_FORMAT="integer")
type_date = TypeData.objects.create(TYD_NAME="Date", TYD_FORMAT="date")
type_tag = TypeData.objects.create(TYD_NAME="Tag", TYD_FORMAT="tag")



# 1er un tableau dynamique
dynamic_table = DynamicTable.objects.create(
    TAB_NAME="Suivi des tâches",
    TAB_DESCRIPTION="Tableau de suivi des tâches du projet frontend",
    SUP_ID=support
)

# Créer des colonnes
col_task = Column.objects.create(COL_NAME="Tâche", COL_ORDER=1, TAB_ID=dynamic_table, TYD_ID=type_text)
col_status = Column.objects.create(COL_NAME="Statut", COL_ORDER=2, TAB_ID=dynamic_table, TYD_ID=type_text)
col_progress = Column.objects.create(COL_NAME="Progression", COL_ORDER=3, TAB_ID=dynamic_table, TYD_ID=type_number)

# Créer des lignes
row1 = Row.objects.create(ROW_NAME="Ligne 1", ROW_ORDER=1, TAB_ID=dynamic_table)
row2 = Row.objects.create(ROW_NAME="Ligne 2", ROW_ORDER=2, TAB_ID=dynamic_table)

# Créer des cellules
Cell.objects.create(CEL_VALUE="Maquettage", COL_ID=col_task, ROW_ID=row1)
Cell.objects.create(CEL_VALUE="En cours", COL_ID=col_status, ROW_ID=row1)
Cell.objects.create(CEL_VALUE="50", COL_ID=col_progress, ROW_ID=row1)

Cell.objects.create(CEL_VALUE="Intégration HTML", COL_ID=col_task, ROW_ID=row2)
Cell.objects.create(CEL_VALUE="À faire", COL_ID=col_status, ROW_ID=row2)
Cell.objects.create(CEL_VALUE="0", COL_ID=col_progress, ROW_ID=row2)



# 2e tableau dynamique
bug_table = DynamicTable.objects.create(
    TAB_NAME="Suivi des bugs",
    TAB_DESCRIPTION="Tableau de suivi des bugs du projet e-commerce",
    SUP_ID=support
)

# Créer des colonnes pour le tableau de bugs
col_bug_id = Column.objects.create(COL_NAME="ID Bug", COL_ORDER=1, TAB_ID=bug_table, TYD_ID=type_number)
col_description = Column.objects.create(COL_NAME="Description", COL_ORDER=2, TAB_ID=bug_table, TYD_ID=type_text)
col_severity = Column.objects.create(COL_NAME="Sévérité", COL_ORDER=3, TAB_ID=bug_table, TYD_ID=type_text)
col_status = Column.objects.create(COL_NAME="Statut", COL_ORDER=4, TAB_ID=bug_table, TYD_ID=type_text)
col_assigned_to = Column.objects.create(COL_NAME="Assigné à", COL_ORDER=5, TAB_ID=bug_table, TYD_ID=type_text)
col_date_reported = Column.objects.create(COL_NAME="Date signalée", COL_ORDER=6, TAB_ID=bug_table, TYD_ID=type_date)

# Créer des lignes pour le tableau de bugs
row1 = Row.objects.create(ROW_NAME="Bug 1", ROW_ORDER=1, TAB_ID=bug_table)
row2 = Row.objects.create(ROW_NAME="Bug 2", ROW_ORDER=2, TAB_ID=bug_table)
row3 = Row.objects.create(ROW_NAME="Bug 3", ROW_ORDER=3, TAB_ID=bug_table)

# Créer des cellules pour le tableau de bugs
# Bug 1
Cell.objects.create(CEL_VALUE="1", COL_ID=col_bug_id, ROW_ID=row1)
Cell.objects.create(CEL_VALUE="Le panier ne se met pas à jour", COL_ID=col_description, ROW_ID=row1)
Cell.objects.create(CEL_VALUE="Élevée", COL_ID=col_severity, ROW_ID=row1)
Cell.objects.create(CEL_VALUE="En cours", COL_ID=col_status, ROW_ID=row1)
Cell.objects.create(CEL_VALUE="Jane Doe", COL_ID=col_assigned_to, ROW_ID=row1)
Cell.objects.create(CEL_VALUE="2024-10-05", COL_ID=col_date_reported, ROW_ID=row1)

# Bug 2
Cell.objects.create(CEL_VALUE="2", COL_ID=col_bug_id, ROW_ID=row2)
Cell.objects.create(CEL_VALUE="Problème d'affichage sur mobile", COL_ID=col_description, ROW_ID=row2)
Cell.objects.create(CEL_VALUE="Moyenne", COL_ID=col_severity, ROW_ID=row2)
Cell.objects.create(CEL_VALUE="À faire", COL_ID=col_status, ROW_ID=row2)
Cell.objects.create(CEL_VALUE="John Doe", COL_ID=col_assigned_to, ROW_ID=row2)
Cell.objects.create(CEL_VALUE="2024-10-07", COL_ID=col_date_reported, ROW_ID=row2)

# Bug 3
Cell.objects.create(CEL_VALUE="3", COL_ID=col_bug_id, ROW_ID=row3)
Cell.objects.create(CEL_VALUE="Erreur 404 sur la page de contact", COL_ID=col_description, ROW_ID=row3)
Cell.objects.create(CEL_VALUE="Faible", COL_ID=col_severity, ROW_ID=row3)
Cell.objects.create(CEL_VALUE="Résolu", COL_ID=col_status, ROW_ID=row3)
Cell.objects.create(CEL_VALUE="Jane Doe", COL_ID=col_assigned_to, ROW_ID=row3)
Cell.objects.create(CEL_VALUE="2024-10-08", COL_ID=col_date_reported, ROW_ID=row3)


# 3e tableau dynamique (pour tester les tags)
task_table = DynamicTable.objects.create(
    TAB_NAME="Tâches avec états",
    TAB_DESCRIPTION="Tableau de suivi des tâches avec états colorés",
    SUP_ID=support
)

# Créer des colonnes dont une avec des tags
col_task = Column.objects.create(COL_NAME="Tâche", COL_ORDER=1, TAB_ID=task_table, TYD_ID=type_text)
col_state = Column.objects.create(COL_NAME="État", COL_ORDER=2, TAB_ID=task_table, TYD_ID=type_tag)

# Créer les options de tags pour la colonne État
tag_options = [
    {"color": "#3498db", "value": "Arrêt"},
    {"color": "#e74c3c", "value": "EnCours"},
    {"color": "#2ecc71", "value": "Fini"}
]

for option in tag_options:
    TagOption.objects.create(
        TAG_COLOR=option["color"],
        TAG_VALUE=option["value"],
        COL_ID=col_state
    )

# Créer des lignes de test
row1 = Row.objects.create(ROW_NAME="Tâche 1", ROW_ORDER=1, TAB_ID=task_table)
row2 = Row.objects.create(ROW_NAME="Tâche 2", ROW_ORDER=2, TAB_ID=task_table)
row3 = Row.objects.create(ROW_NAME="Tâche 3", ROW_ORDER=3, TAB_ID=task_table)

# Créer des cellules avec les différents états
Cell.objects.create(CEL_VALUE="Développement API", COL_ID=col_task, ROW_ID=row1)
Cell.objects.create(CEL_VALUE="EnCours", COL_ID=col_state, ROW_ID=row1)

Cell.objects.create(CEL_VALUE="Tests unitaires", COL_ID=col_task, ROW_ID=row2)
Cell.objects.create(CEL_VALUE="Arrêt", COL_ID=col_state, ROW_ID=row2)

Cell.objects.create(CEL_VALUE="Documentation", COL_ID=col_task, ROW_ID=row3)
Cell.objects.create(CEL_VALUE="Fini", COL_ID=col_state, ROW_ID=row3)

# Exemple d'utilisation de add_column avec des tags
task_table.add_column(
    "Priorité",
    "Tag",
    tag_options={
        "#ff0000": "Haute",
        "#ffaa00": "Moyenne",
        "#00ff00": "Basse"
    }
)

print("Nouvelles données remplies.")