from django.urls import include, path
from .views import *


urlpatterns = [
    path('createschema/', create_schema, name = 'create-schema'),
    path('listschema/', list_schema, name = 'listschema'),
    path('<pk>/', create_column, name = 'create-column'),
    path('htmx/column-form/',create_column_form, name='column-form'),
    path('htmx/column/<pk>/',detail_column, name='detail-column'),
    path('htmx/schema/<pk>/delete',delete_scheme, name='delete-scheme'),
    path('htmx/schema/<pk>/edit',edit_scheme, name='edit-scheme'),
    path('generatecsv/<pk>/',generate_csv, name="generate-csv")
]