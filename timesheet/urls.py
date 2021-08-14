from django.urls import path
from django.views.generic.base import View
from .views import TimesheetListView, TimesheetCreateView, TimesheetUpdateView




urlpatterns = [
    path('', TimesheetListView.as_view(), name='overview_timesheet'),
    path('create/', TimesheetCreateView.as_view(), name='timesheet_view_create'), 
    path('update/<int:pk>/', TimesheetUpdateView.as_view(), name='timesheet_view_update'), 
]