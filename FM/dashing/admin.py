from django.contrib import admin
from .models import Task, Query


# Register your models here.
#admin.site.register(Task)
#admin.site.register(Query)

class QueryInline(admin.TabularInline):
    model = Query

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency']
    inlines = [QueryInline]

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_filter = ['task', 'status']
    list_display = ['task', 'price_starts', 'price_ends', 'target_amount', 'status']
