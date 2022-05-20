from django.contrib import admin
from .models import Schema, Column

class ColumnInlineAdmin(admin.TabularInline):
    model = Column
    extra = 5

class SchemaAdmin(admin.ModelAdmin):
    inlines = [ColumnInlineAdmin]

admin.site.register(Schema, SchemaAdmin)
