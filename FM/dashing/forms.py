from django.forms import ModelForm
from .models import Task, Query, Notification


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['currency']


class QueryForm(ModelForm):
    class Meta:
        model = Query
        fields = ['task', 'price_starts', 'price_ends', 'target_amount']


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['query', 'message']
