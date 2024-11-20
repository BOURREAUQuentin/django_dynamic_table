from django.db import models

class Category(models.Model):
    CAT_ID = models.AutoField(primary_key=True)
    CAT_NAME = models.CharField(max_length=100)

    def __str__(self):
        return self.CAT_NAME

class Artist(models.Model):
    ART_ID = models.AutoField(primary_key=True)
    ART_NAME = models.CharField(max_length=100)
    ART_FIRSTNAME = models.CharField(max_length=100)
    ART_LASTNAME = models.CharField(max_length=100)
    ART_EMAIL = models.EmailField()
    ART_TEL = models.CharField(max_length=20)
    ART_PASSWORD = models.CharField(max_length=100)
    ART_BIOGRAPHY = models.TextField()

    def __str__(self):
        return f"{self.ART_FIRSTNAME} {self.ART_LASTNAME}"

class Document(models.Model):
    DOC_ID = models.AutoField(primary_key=True)
    DOC_NAME = models.CharField(max_length=100)
    DOC_INFORMATION = models.TextField()
    ART_ID = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.DOC_NAME

class Project(models.Model):
    PRJ_ID = models.AutoField(primary_key=True)
    PRJ_NAME = models.CharField(max_length=100)
    PRJ_FORMAT = models.CharField(max_length=50)
    PRJ_DUE_DATE = models.DateField()
    DOC_ID = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.PRJ_NAME

class Support(models.Model):
    SUP_ID = models.AutoField(primary_key=True)
    SUP_NAME = models.CharField(max_length=100)
    SUP_DURATION = models.DurationField()
    SUP_PROGRESS = models.FloatField()
    PRJ_ID = models.ForeignKey(Project, on_delete=models.CASCADE)
    CAT_ID = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.SUP_NAME

class TypeData(models.Model):
    TYD_ID = models.AutoField(primary_key=True)
    TYD_NAME = models.CharField(max_length=100)
    TYD_FORMAT = models.CharField(max_length=50)

    def __str__(self):
        return self.TYD_NAME

class DynamicTable(models.Model):
    TAB_ID = models.AutoField(primary_key=True)
    TAB_NAME = models.CharField(max_length=100)
    TAB_DESCRIPTION = models.TextField()
    SUP_ID = models.ForeignKey(Support, on_delete=models.CASCADE)

    def add_column(self, col_name, typ_name):
        # récupère l'ordre de la dernière colonne
        last_col = Column.objects.filter(TAB_ID=self).order_by('-COL_ORDER').first()
        new_col_order = last_col.COL_ORDER + 1 if last_col else 1

        # crée la nouvelle colonne
        new_column = Column.objects.create(
            COL_NAME=col_name,
            COL_ORDER=new_col_order,
            TAB_ID=self,
            TYD_ID=TypeData.objects.filter(TYD_NAME=typ_name).first()
        )

        # crée une nouvelle cellule pour chaque ligne existante
        rows = Row.objects.filter(TAB_ID=self)
        for row in rows:
            Cell.objects.create(
                CEL_VALUE="",
                COL_ID=new_column,
                ROW_ID=row
            )

        return new_column

    def add_row(self):
        # récupère l'ordre de la dernière ligne
        last_row = Row.objects.filter(TAB_ID=self).order_by('-ROW_ORDER').first()
        new_row_order = last_row.ROW_ORDER + 1 if last_row else 1

        # crée la nouvelle ligne
        new_row = Row.objects.create(
            ROW_NAME=f"Nouvelle ligne {new_row_order}",
            ROW_ORDER=new_row_order,
            TAB_ID=self
        )

        # crée une nouvelle cellule pour chaque colonne
        columns = Column.objects.filter(TAB_ID=self)
        for column in columns:
            Cell.objects.create(
                CEL_VALUE="",
                COL_ID=column,
                ROW_ID=new_row
            )

        return new_row

    def __str__(self):
        return self.TAB_NAME

class Column(models.Model):
    COL_ID = models.AutoField(primary_key=True)
    COL_NAME = models.CharField(max_length=100)
    COL_ORDER = models.IntegerField()
    TAB_ID = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)
    TYD_ID = models.ForeignKey(TypeData, on_delete=models.CASCADE)

    def __str__(self):
        return self.COL_NAME

class Row(models.Model):
    ROW_ID = models.AutoField(primary_key=True)
    ROW_NAME = models.CharField(max_length=100)
    ROW_ORDER = models.IntegerField()
    TAB_ID = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)

    def __str__(self):
        return self.ROW_NAME

class Cell(models.Model):
    CEL_ID = models.AutoField(primary_key=True)
    CEL_VALUE = models.TextField()
    COL_ID = models.ForeignKey(Column, on_delete=models.CASCADE)
    ROW_ID = models.ForeignKey(Row, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cell {self.CEL_ID}"

class Employee(models.Model):
    EMP_ID = models.AutoField(primary_key=True)
    EMP_FIRSTNAME = models.CharField(max_length=100)
    EMP_LASTNAME = models.CharField(max_length=100)
    EMP_EMAIL = models.EmailField()
    EMP_TEL = models.CharField(max_length=20)
    EMP_PASSWORD = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.EMP_FIRSTNAME} {self.EMP_LASTNAME}"
