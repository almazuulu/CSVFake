from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .models import Schema, Column
from .forms import ColumnForm, ColumnFormSet, SchemaForm


def create_column(request, pk):
    schema = Schema.objects.get(id=pk)
    columns = Column.objects.filter(schema_name=schema)
    form = SchemaForm(request.POST or None)
    columnForm = ColumnForm(request.POST or None)

    #ColumnFormSet = inlineformset_factory(Schema, Column, fields={'column_name','type_column','order'}, extra=10 )
    #formset = ColumnFormSet(request.POST or None)
    if request.method == "POST":
        if form.is_valid() and columnForm.is_valid():
            form.save(commit=False)
            # column.schema_name = schema
            # column.save()
            # return redirect("detail-form", pk=column.id)

            column = columnForm.save(commit=False)
            column.schema_name = schema
            column.save()
            return redirect('detail-form',pk=column.id)
        else:
            return render(request, "partials/column_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "schema":schema,
        "columns": columns
    }

    return render(request, "create_column.html", context)

def create_column_form(request):
    form = ColumnForm()

    context = {
        "form": form
    }
    return render(request, "partials/column_form.html", context)

def detail_column(request, pk):
    column = Column.objects.get(pk=pk)
    context = {
        "column": column
    }
    return render(request, "partials/column_form.html", context)