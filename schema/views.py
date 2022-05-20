from django.shortcuts import render, redirect
from .models import Schema, Column
from .forms import ColumnForm, ColumnFormSet

def create_column(request, pk):
    schema = Schema.objects.get(pk = pk)
    formset = ColumnFormSet(request.POST or None)

    if request.method == "POST":
        if formset.is_valid():
            formset.instance = schema
            formset.save()
        return redirect('create-column', pk=schema.id)
    context = {
        "formset":formset,
        "schema":schema
    }

    return render(request, 'create_column.html', context)
