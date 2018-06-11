from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task, Query, Notification
from .forms import TaskForm, QueryForm
from api_manager.api.api import BitCoinApi
from django_ajax.decorators import ajax


# Create your views here.
@ajax
def btc(request):
    c = 2 + 3
    return {'result': c}




class TaskListView(ListView):
    model = Task


class TaskDetailView(DetailView):
    model = Task


class TaskCreate(CreateView):
    model = Task
    fields = ['currency']
    success_url = reverse_lazy('query_create')


class TaskUpdate(UpdateView):
    model = Task
    fields = ['currency']


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')


class QueryListView(ListView):
    model = Query


class QueryDetailView(DetailView):
    model = Query


class QueryCreate(CreateView):
    model = Query
    fields = ['task', 'price_starts', 'price_ends', 'target_amount']
    success_url = reverse_lazy('querys')


class QueryUpdate(UpdateView):
    model = Query
    fields = ['price_starts', 'price_ends', 'target']


class QueryDelete(DeleteView):
    model = Query
    success_url = reverse_lazy('querys')


class DashingView(TemplateView):
    template_name = 'dashing.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['task_list'] = Task.objects.all()
        context['query_list'] = Query.objects.all()
        context['task_form'] = TaskForm()
        context['query_form'] = QueryForm()
        return context

class NotificationListView(ListView):
    model = Notification
