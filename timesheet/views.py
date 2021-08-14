from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView 
from .models import TimesheetModel
from django.contrib.auth.mixins import (
    LoginRequiredMixin, # To restrict view access to only logged in users
    UserPassesTestMixin # To restrict access
)
from django.core.exceptions import PermissionDenied
from datetime import datetime 
from django.shortcuts import render
from django.template import RequestContext


class TimesheetListView(LoginRequiredMixin, ListView):
    template_name = 'timesheet/overview_timesheet.html'
    model = TimesheetModel
    paginate_by = 15

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super(TimesheetListView, self).get_queryset().order_by('-id')
        return super(TimesheetListView, self).get_queryset().filter(author=self.request.user).order_by('-id')


# Creating an timesheet using 'timesheet_new.html'
class TimesheetCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = TimesheetModel
    template_name = 'timesheet/create.html'
    fields = ('from_hour','to_hour', 'description',)
    
    # PermissionDenied for dublicated record
    def test_func(self):
            if self.request.user.is_anonymous:
                raise PermissionDenied("You are not authenticated! Please login first.")
            elif self.request.user.is_superuser:
                raise PermissionDenied("You don't have permission to create a new Timesheet")
            elif TimesheetModel.objects.filter(author=self.request.user, date=datetime.now()).exists():
                raise PermissionDenied("You have set your timesheet today!, Please come back tomorrow.")
            else:
                return True

    # set current author automatically
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TimesheetUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = TimesheetModel
    fields = ('from_hour','to_hour', 'description',)
    template_name = 'timesheet/update.html'

    # PermissionDenied for updating not exsisted record
    def test_func(self):
            if self.request.user.is_anonymous:
                raise PermissionDenied("You are not authenticated! Please login first.")
            elif TimesheetModel.objects.filter(date=datetime.now(),id=self.kwargs['pk'], author=self.request.user) :
                return True
            else:
                raise PermissionDenied("You are only able to update your current day record!, We are sorry for that.")


def handler404(request):
    response = render('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 404
    return response