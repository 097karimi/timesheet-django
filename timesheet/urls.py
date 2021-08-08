from django.urls import path
from django.views.generic.base import View
from .views import TimesheetListView, TimesheetCreateView


urlpatterns = [
    path('', TimesheetListView.as_view(), name='overview_timesheet'),
    path('create/', TimesheetCreateView.as_view(), name='timesheet_view'), 
]