from django.urls import include, path
from .views import *


urlpatterns = [
    path('<pk>/', create_column, name = 'create-column'),
    path('htmx/column-form/',create_column_form, name='column-form'),
    path('htmx/column/<pk>/',detail_column, name='detail-form')
]