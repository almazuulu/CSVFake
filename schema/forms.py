from django import forms
from django.forms.models import inlineformset_factory
from .models import Column, Schema

class ColumnForm(forms.ModelForm):
    class Meta:
        fields = "__all__"


ColumnFormSet  = inlineformset_factory(
    Schema,
    Column,
    ColumnForm,
    can_delete=True,
    min_num= 5,
    extra= 0
)
