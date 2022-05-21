from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
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
            # schema = schemaform.save()
            # if form.is_valid():
            #     schema = schemaform.save()
            #     column = form.save(commit=False)
            #     column.schema_name = schema
            #     column.save()
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

# def create_column(request, pk):
#     schema = Schema.objects.get(id=pk)
#     columns = Column.objects.filter(schema_name=schema)
#     form = SchemaForm(request.POST or None)
#     columnForm = ColumnForm(request.POST or None)
#
#     #ColumnFormSet = inlineformset_factory(Schema, Column, fields={'column_name','type_column','order'}, extra=10 )
#     #formset = ColumnFormSet(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid() and columnForm.is_valid():
#             form.save(commit=False)
#             # column.schema_name = schema
#             # column.save()
#             # return redirect("detail-form", pk=column.id)
#
#             column = columnForm.save(commit=False)
#             column.schema_name = schema
#             column.save()
#             return redirect('detail-column',pk=column.id)
#         else:
#             return render(request, "partials/column_form.html", context={
#                 "form": form,
#                 "columnForm":columnForm
#             })
#
#     context = {
#         "form": form,
#         "schema":schema,
#         "columns": columns
#     }
#
#     return render(request, "create_column.html", context)

# def create_column_form(request):
#     form = SchemaForm(request.POST or None)
#     columnForm = ColumnForm(request.POST or None)
#
#     context = {
#         "form": form,
#         "columnForm":columnForm
#     }
#     return render(request, "partials/column_form.html", context)
def create_column_form(request):

    form = ColumnForm(request.POST or None)
    context = {
              "form": form
             }
    return render(request, "partials/column_form.html", context)


def detail_column(request, pk):
    column = get_object_or_404(Column, id=pk)
    context = {
        "column": column
    }
    return render(request, "partials/detail_column.html", context)