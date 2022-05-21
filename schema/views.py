from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Schema, Column
from .forms import ColumnForm, ColumnFormSet, SchemaForm

def create_schema(request):
    schemaform = SchemaForm(request.POST or None)
    formset = ColumnFormSet(request.POST or None)
    form = ColumnForm(request.POST or None)
    # columns = Column.objects.filter(schema_name=schemaform)
    if request.method == "POST":
        if formset.is_valid() and schemaform.is_valid():
            schema = schemaform.save()
            formset.instance = schema
            formset.save()

            if form.is_valid():
                column = form.save(commit=False)
                column.schema_name = schema
                column.save()
            return redirect("create-schema")
        else:
            return render(request, "partials/column_form.html", context={
                "form": form
            })
    # else:
    context = {
        "schemaform": schemaform,
        "formset": formset,
        "form": form
    }
    return render(request, 'create_schema.html', context)

def create_column(request, pk):
    schema = Schema.objects.get(id=pk)
    columns = Column.objects.filter(schema_name=schema)
    form = ColumnForm(request.POST or None)
    formset = ColumnFormSet(request.POST or None)

    if request.method == "POST":
        if (form.is_valid()) and (form.is_valid()):
            formset.instance = schema
            formset.save()

            column = form.save(commit=False)
            column.schema_name = schema
            column.save()

            return redirect("detail-column", pk=column.id)


    context = {
        "form": form,
        "formset": formset,
        "schema": schema,
        "columns": columns
    }

    return render(request, "create_column.html", context)

def create_column_form(request):

    form = ColumnForm(request.POST or None)
    context = {
              "form": form
             }
    return render(request, "partials/column_form.html", context)

def list_schema(request):
    schemas = Schema.objects.all()
    context = {
        "schemas":schemas
    }
    return render(request, 'list_schema.html', context)


def detail_column(request, pk):
    column = get_object_or_404(Column, id=pk)
    context = {
        "column": column
    }
    return render(request, "partials/detail_column.html", context)

def delete_scheme(request, pk):
    schema = Schema.objects.get(pk = pk)
    schema.delete()

    return HttpResponse('')

def edit_scheme(request, pk):
    scheme = Schema.objects.get(pk=pk)
    schemaform = SchemaForm(request.POST or None, instance=scheme)
    formset = ColumnFormSet(request.POST or None, instance=scheme)
    form = ColumnForm(request.POST or None, instance=scheme)
    # columns = Column.objects.filter(schema_name=schemaform)
    if request.method == "POST":
        if formset.is_valid() and schemaform.is_valid():
            schema = schemaform.save()
            formset.instance = schema
            formset.save()

            if form.is_valid():
                column = form.save()
                return redirect("listschema")
        return redirect('listschema')
    context = {
        "schemaform": schemaform,
        "formset": formset,
        "scheme":scheme
    }
    return render(request,"create_schema.html", context)