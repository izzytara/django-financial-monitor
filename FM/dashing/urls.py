from django.urls import path, include
from . import views

urlpatterns = [
    path('btc/', views.btc, name='btc'),
    path('', views.DashingView.as_view(), name='dashing'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create', views.TaskCreate.as_view(), name='task_create'),
    path('task/<int:pk>/update', views.TaskUpdate.as_view(), name='task_update'),
    path('task/<int:pk>/delete', views.TaskDelete.as_view(), name='task_delete'),
    path('querys/', views.QueryListView.as_view(), name='querys'),
    path('query/<int:pk>', views.QueryDetailView.as_view(), name='query-detail'),
    path('query/create', views.QueryCreate.as_view(), name='query_create'),
    path('query/<int:pk>/update', views.QueryUpdate.as_view(), name='query_update'),
    path('query/<int:pk>/delete', views.QueryDelete.as_view(), name='query_delete'),
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
]