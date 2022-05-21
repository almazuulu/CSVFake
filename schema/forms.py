from django import forms
from django.forms.models import inlineformset_factory
from .models import Column, Schema

class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields=('column_name','type_column','order')

class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = "__all__"


ColumnFormSet  = inlineformset_factory(
    Schema,
    Column,
    ColumnForm,
    can_delete=True,
    min_num= 2,
    extra= 0
)
