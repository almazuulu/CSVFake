from itertools import cycle
from random import randint

from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from faker import Faker
import csv



from .models import Schema, Column
from .forms import ColumnForm, ColumnFormSet, SchemaForm

def create_schema(request):
    schemaform = SchemaForm(request.POST or None)
    formset = ColumnFormSet(request.POST or None)
    form = ColumnForm(request.POST or None)
    # columns = Column.objects.filter(schema_name=schemaform)
    if request.method == "POST":
        if all([formset.is_valid(), schemaform.is_valid()]):
            schema = schemaform.save()
            formset.instance = schema
            formset.save()

            if form.is_valid():
                column = form.save(commit=False)
                column.schema_name = schema
                column.save()
            return redirect("listschema")
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

    context = {
        "schemaform": schemaform,
        "formset": formset,
        "scheme": scheme
    }
    if request.method == "POST":
        if all([formset.is_valid(), schemaform.is_valid()]):
            schema = schemaform.save()
            formset.instance = schema
            formset.save()

            if form.is_valid():
                column = form.save(commit=False)
                column.schema_name = schema
                column.save()
            # return redirect("listschema")
            return HttpResponseRedirect(reverse('listschema'))

        if request.htmx:
            return HttpResponseRedirect(reverse('listschema'))

    return render(request,"create_schema.html", context)

def generate_csv(request, pk):
    schema = Schema.objects.get(pk=pk)
    filename = schema.name
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    writer = csv.writer(response)

    listData = []

    for i in schema.column_set.all():
        listData.append([i.column_name, i.order, i.type_column])

    listData.sort(key=lambda x: x[1])
    listDataCSV = [i[0] for i in listData]
    print(listDataCSV)

    fake = Faker()
    name_person = cycle([fake.name(), fake.name()])
    rows = []

    #actual names from schemas, not type
    full_name_person = " "
    job_name = " "
    email_address = " "
    domain_name = " "
    tel_number = " "
    company_name = " "
    text_content = " "
    integerValue = 0
    address_value = " "
    date_value = " "

    for i in listData:
        if i[2] == 'Full name':
            full_name_person = i[0]
        elif i[2] == 'Job':
            job_name = i[0]
        elif i[2] == 'Email':
            email_address = i[0]
        elif i[2] == 'Domain name':
            domain_name = i[0]
        elif i[2] == 'Phone number':
            tel_number = i[0]
        elif i[2] == 'Company name':
            company_name = i[0]
        elif i[2] == 'Text':
            text_content = i[0]
        elif i[2] == 'Integer':
            integerValue = i[0]
        elif i[2] == 'Address':
            address_value = i[0]
        elif i[2] == 'Date':
            date_value = i[0]


    listOfTupleDict = []
    for i in range(5):
        for i in listDataCSV:
            if i == full_name_person:
                listOfTupleDict.append((full_name_person, next(name_person)))
            elif i == job_name:
                listOfTupleDict.append((job_name, fake.job()))
            elif i == email_address:
                listOfTupleDict.append((email_address, fake.email(domain=fake.url())))
            elif i == domain_name:
                listOfTupleDict.append((domain_name, fake.url()))
            elif i == tel_number:
                listOfTupleDict.append((tel_number, fake.phone_number()))
            elif i == company_name:
                listOfTupleDict.append((company_name, fake.company()))
            elif i == text_content:
                listOfTupleDict.append((text_content, fake.sentence(nb_words=10)))
            elif i == integerValue:
                listOfTupleDict.append((text_content, randint(0, 10)))
            elif i == address_value:
                address_data = fake.country()+ " "+fake.city()+" " + fake.street_address()
                listOfTupleDict.append((address_value, address_data ))
            elif i == date_value:
                listOfTupleDict.append((date_value, fake.date()))

        someDict = dict(listOfTupleDict)
        rows.append(someDict)

    fake_listData = [list(rows[i].values()) for i in range(len(rows))]
    writer.writerow(listDataCSV)
    for data in fake_listData:
        writer.writerow(data)

    return response

